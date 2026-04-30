# -*- coding: utf-8 -*-
"""
Build compile/module_scripts.py from src/scripts fragments (vanilla-compatible).

v41D additions:
- Fast fail: syntax-check every fragment with compile() to pinpoint errors early.
- Better error localization: emit source-mapping comments before each script entry:
    # [src/scripts/.../file.py:Lx-Ly] script_id
  These comments make it much easier to trace Warband compiler errors back to
  the modular fragment that produced the offending lines.

Ordering policy:
- Folder-driven order for everything by default (sorted relative paths).
- ZA_hardcoded_game_scripts can optionally enforce a strict order via:
    src/scripts/ZA_hardcoded_game_scripts/_order_za_scripts.txt
  (This keeps the "hardcoded game scripts" stable without forcing templates.)
- Filenames are semantic; section codes live in folder names.
"""
from __future__ import annotations

import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "scripts"
OUT = ROOT / "compile" / "module_scripts.py"

# Incremental build cache (v41B): skip regeneration if inputs unchanged
CACHE_SCHEMA_VERSION = 1
CACHE_DIR = ROOT / ".buildcache"
CACHE_FILE = CACHE_DIR / "scripts_manifest.json"

# Optional: user-defined preamble lines live here.
# If present, they replace the hardcoded import block below.
PREAMBLE_DIR = SRC / "_preamble"

ZA_ORDER_FILE = SRC / "ZA_hardcoded_game_scripts" / "_order_za_scripts.txt"

# ----------------------------
# Helpers: folder tags -> banners / index
# ----------------------------

_CODE_RE = re.compile(r"^(Z[A-Z])_([^/]+)$")
_SUB_RE  = re.compile(r"^(Z[A-Z]\d{2})_([^/]+)$")


def _prettify(label: str) -> str:
    return label.replace("_", " ").strip()


def parse_codes_from_path(parts: List[str]) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Given relative folder parts (excluding filename), return:
      (top_code, top_label, sub_code, sub_label)
    Example parts:
      ["ZH_heroes", "ZH06_companions"] -> ("ZH","heroes","ZH06","companions")
    """
    top_code = top_label = sub_code = sub_label = None
    for p in parts:
        m = _CODE_RE.match(p)
        if m:
            top_code, top_label = m.group(1), m.group(2)
            continue
        m = _SUB_RE.match(p)
        if m:
            sub_code, sub_label = m.group(1), m.group(2)
            continue
    return top_code, top_label, sub_code, sub_label


def _syntax_check_fragment(fp: Path, raw: str) -> None:
    """Fast-fail syntax check with precise file/line reporting."""
    try:
        compile(raw, fp.as_posix(), "exec")
    except SyntaxError as e:
        lines = raw.splitlines()
        lineno = int(getattr(e, "lineno", 0) or 0)
        offset = int(getattr(e, "offset", 0) or 0)
        msg = getattr(e, "msg", "SyntaxError")

        # Context snippet
        start = max(1, lineno - 2)
        end = min(len(lines), lineno + 2)
        snippet = []
        for i in range(start, end + 1):
            prefix = ">" if i == lineno else " "
            snippet.append(f"{prefix}{i:4d}| {lines[i-1]}")
        sn = "\n".join(snippet)

        rel = fp.relative_to(ROOT).as_posix() if fp.is_absolute() else fp.as_posix()
        raise SystemExit(
            f"[build_scripts] FAIL: {rel}:{lineno}:{offset} {msg}\n{sn}"
        )


def extract_list_block_span(raw: str, var_name: str) -> Tuple[str, int]:
    """
    Return (inner_text, base_line) for: VAR = [ ... ]

    - inner_text is the exact substring between '[' and the matching ']' (NOT stripped)
    - base_line is the 1-based line number of the line containing the '['.

    The state machine handles strings and # comments to avoid bracket confusion.
    """
    m = re.search(rf"^\s*{re.escape(var_name)}\s*=\s*\[", raw, re.MULTILINE)
    if not m:
        raise ValueError(f"Missing {var_name} assignment in fragment.")
    lb = raw.find("[", m.start())
    if lb < 0:
        raise ValueError(f"Missing '[' after {var_name}.")

    i = lb
    depth = 0
    in_str = False
    str_ch = ""
    esc = False
    in_comment = False

    while i < len(raw):
        ch = raw[i]

        if in_comment:
            if ch == "\n":
                in_comment = False
            i += 1
            continue

        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == str_ch:
                in_str = False
            i += 1
            continue

        if ch == "#":
            in_comment = True
            i += 1
            continue
        if ch in ("'", '"'):
            in_str = True
            str_ch = ch
            i += 1
            continue

        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                base_line = raw.count("\n", 0, lb) + 1
                return raw[lb + 1 : i], base_line
        i += 1

    raise ValueError(f"Unclosed list bracket for {var_name}.")


def extract_script_name_from_fragment(raw: str) -> Optional[str]:
    """Return first script id in SCRIPTS list, or None if fragment doesn't export SCRIPTS."""
    if "SCRIPTS" not in raw:
        return None
    try:
        inner, _ = extract_list_block_span(raw, "SCRIPTS")
    except ValueError:
        return None
    m = re.search(r'^\s*\(\s*"([^"]+)"\s*,', inner, re.MULTILINE)
    return m.group(1) if m else None


def _strip_legacy_import_shim_block(text: str) -> str:
    """
    Remove the old src.compiler / src.module_system compatibility shim from a
    fragment preamble while preserving any real helper imports and functions.

    The shim is usually a leading top-level try/except block copied from the
    classic module system. It is safe to drop when generating compile outputs
    because the builder already provides the correct runtime imports.

    Also remove any fragment-local ``from __future__ import ...`` lines, since
    future imports are only valid at the top of a Python module and fragment
    preambles are injected mid-file in the generated output.
    """
    lines = text.splitlines()
    first_nonempty = None
    for idx, line in enumerate(lines):
        if line.strip():
            first_nonempty = idx
            break

    if first_nonempty is None:
        return ""

    first_line = lines[first_nonempty].strip()
    if not (
        first_line in ("try:", "except:", "except ImportError:")
        or "src.compiler" in first_line
        or "src.module_system" in first_line
    ):
        cleaned = text.rstrip()
        return "\n".join(
            line for line in cleaned.splitlines()
            if not line.lstrip().startswith("from __future__ import ")
        ).rstrip()

    kept = []
    skipping = True
    for line in lines:
        stripped = line.strip()
        if skipping:
            if not stripped:
                continue
            if stripped in ("try:", "except:", "except ImportError:"):
                continue
            if "src.compiler" in stripped or "src.module_system" in stripped:
                continue
            skipping = False
        kept.append(line)

    return "\n".join(
        line for line in kept
        if not line.lstrip().startswith("from __future__ import ")
    ).rstrip()


def extract_fragment_preamble_block(raw: str) -> str:
    """
    Return the top-level fragment body that appears before SCRIPTS = [ ... ].

    This preserves helper functions and imports defined above the script table so
    they remain available to the generated module before the merged scripts list
    is evaluated.
    """
    m = re.search(r"^\s*SCRIPTS\s*=\s*\[", raw, re.MULTILINE)
    if not m:
        return ""
    return _strip_legacy_import_shim_block(raw[:m.start()].rstrip())


def read_order_list(path: Path) -> List[str]:
    if not path.exists():
        return []
    lines: List[str] = []
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        lines.append(ln.replace("\\", "/"))
    return lines


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _builder_fingerprint() -> str:
    # Invalidate cache when this builder changes
    return _sha256_file(Path(__file__).resolve())


def _sig_for(path: Path) -> Dict[str, object]:
    st = path.stat()
    return {
        "rel": path.relative_to(SRC).as_posix(),
        "mtime_ns": int(getattr(st, "st_mtime_ns", int(st.st_mtime * 1e9))),
        "size": int(st.st_size),
    }


def _load_cache() -> Optional[dict]:
    if not CACHE_FILE.exists():
        return None
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def _write_cache(payload: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def build_index(all_files: List[Path]) -> List[str]:
    """Build a compact, searchable index header based on folder codes."""
    seen_top: Dict[str, str] = {}
    seen_sub: Dict[Tuple[str, str], str] = {}

    for fp in all_files:
        rel = fp.relative_to(SRC)
        parts = list(rel.parts[:-1])
        top_code, top_label, sub_code, sub_label = parse_codes_from_path(parts)
        if top_code and top_label:
            seen_top.setdefault(top_code, _prettify(top_label))
        if top_code and sub_code and sub_label:
            seen_sub.setdefault((top_code, sub_code), _prettify(sub_label))

    lines = []
    lines.append("# Table of Contents (generated from src/scripts folders):")
    lines.append("#")
    for top_code in sorted(seen_top.keys()):
        lines.append(f"#   _{top_code}_ - {seen_top[top_code]}")
        subs = [(sub, seen_sub[(top_code, sub)]) for (t, sub) in seen_sub.keys() if t == top_code]
        subs.sort(key=lambda x: x[0])
        for sub, lab in subs:
            lines.append(f"# [ {sub} ] - {lab}")
    lines.append("#")
    return lines


def order_files_folder_driven() -> List[Path]:
    # NOTE: _preamble is reserved for header imports and must not be treated as fragments.
    all_files = [
        p
        for p in SRC.rglob("*.py")
        if p.is_file() and "_preamble" not in p.parts
    ]
    # Deterministic ordering across OSes:
    all_files.sort(key=lambda p: p.relative_to(SRC).as_posix().lower())
    return all_files


def load_preamble_lines() -> List[str]:
    """Load preamble lines from src/scripts/_preamble/*.py, if any."""
    if not PREAMBLE_DIR.exists():
        return []

    files = [p for p in PREAMBLE_DIR.glob("*.py") if p.is_file()]
    files.sort(key=lambda p: p.name.lower())

    lines: List[str] = []
    for fp in files:
        raw = fp.read_text(encoding="utf-8", errors="replace").splitlines()
        for ln in raw:
            ln = ln.rstrip()
            if ln and not ln.lstrip().startswith("from __future__ import "):
                lines.append(ln)
    return lines


def apply_za_order(all_files: List[Path]) -> List[Path]:
    """If _order_za_scripts.txt exists, reorder only ZA files accordingly."""
    if not ZA_ORDER_FILE.exists():
        return all_files

    za_files = [p for p in all_files if "ZA_hardcoded_game_scripts" in p.parts]
    other_files = [p for p in all_files if p not in za_files]

    rel_to_src = {str(p.relative_to(SRC)).replace("\\", "/"): p for p in za_files}

    ordered: List[Path] = []
    for rel in read_order_list(ZA_ORDER_FILE):
        p = rel_to_src.get(rel)
        if p:
            ordered.append(p)

    listed = set(ordered)
    ordered += [p for p in za_files if p not in listed]

    return ordered + other_files


def _split_script_entries(inner: str, base_line: int) -> List[Tuple[str, int, int, str]]:
    """Split inner SCRIPTS list content into per-script chunks.

    Returns list of tuples: (chunk_text, start_line, end_line, script_id)
    Line numbers are 1-based in the original fragment file.
    """
    lines = inner.splitlines()

    starts: List[Tuple[int, str]] = []
    rx = re.compile(r'^\s*\(\s*"([^"]+)"\s*,')

    for i, ln in enumerate(lines):
        m = rx.match(ln)
        if m:
            starts.append((i, m.group(1)))

    if not starts:
        return []

    chunks: List[Tuple[str, int, int, str]] = []

    for idx, (s_i, sid) in enumerate(starts):
        e_i = (starts[idx + 1][0] - 1) if (idx + 1) < len(starts) else (len(lines) - 1)

        # Trim trailing blank lines within the chunk for nicer mapping.
        while e_i > s_i and (lines[e_i].strip() == ""):
            e_i -= 1

        chunk_lines = lines[s_i : e_i + 1]

        # Ensure the chunk ends with a comma (Warband module system expects comma-separated tuples).
        # Add comma to the last non-empty line if missing.
        k = len(chunk_lines) - 1
        while k >= 0 and chunk_lines[k].strip() == "":
            k -= 1
        if k >= 0 and not chunk_lines[k].rstrip().endswith(","):
            chunk_lines[k] = chunk_lines[k].rstrip() + ","

        chunk_text = "\n".join(chunk_lines).rstrip()
        start_line = base_line + s_i
        end_line = base_line + e_i

        chunks.append((chunk_text, start_line, end_line, sid))

    return chunks


def build(use_cache: bool = True, emit_source_map: bool = True) -> None:
    if not SRC.exists():
        raise SystemExit(f"Missing source folder: {SRC}")

    all_files = order_files_folder_driven()
    all_files = apply_za_order(all_files)

    # v41B: Incremental cache (scripts only)
    if use_cache and OUT.exists():
        preamble_files: List[Path] = []
        if PREAMBLE_DIR.exists():
            preamble_files = [p for p in PREAMBLE_DIR.glob("*.py") if p.is_file()]
            preamble_files.sort(key=lambda p: p.name.lower())

        za_sig = _sig_for(ZA_ORDER_FILE) if ZA_ORDER_FILE.exists() else None

        current = {
            "schema": CACHE_SCHEMA_VERSION,
            "builder_sha256": _builder_fingerprint(),
            "emit_source_map": bool(emit_source_map),
            "fragments": [_sig_for(p) for p in all_files],
            "preamble": [_sig_for(p) for p in preamble_files],
            "za_order": za_sig,
        }
        prev = _load_cache()
        if prev == current:
            print("[build_scripts] Up-to-date; skipped (cache)")
            return

    # Fast-fail syntax checks + duplicate detection by script name
    script_to_path: Dict[str, Path] = {}
    fragment_preamble_lines: List[str] = []
    for fp in all_files:
        raw = fp.read_text(encoding="utf-8", errors="replace")
        _syntax_check_fragment(fp, raw)

        preamble_block = extract_fragment_preamble_block(raw)
        if preamble_block.strip():
            fragment_preamble_lines.append(f"# --- {fp.relative_to(SRC).as_posix()} preamble ---")
            fragment_preamble_lines.extend(
                line for line in preamble_block.splitlines()
                if not line.lstrip().startswith("from __future__ import ")
            )
            fragment_preamble_lines.append("")

        name = extract_script_name_from_fragment(raw)
        if not name:
            continue
        if name in script_to_path:
            raise SystemExit(f"Duplicate script fragment for '{name}':\n  {script_to_path[name]}\n  {fp}")
        script_to_path[name] = fp

    # Header + preamble imports
    preamble = load_preamble_lines()
    if not preamble:
        preamble = [
            "from header_common import *",
            "from header_operations import *",
            "from module_constants import *",
            "from header_parties import *",
            "from header_skills import *",
            "from header_mission_templates import *",
            "from header_items import *",
            "from header_quests import *",
            "from header_triggers import *",
            "from header_terrain_types import *",
            "from header_music import *",
            "from header_map_icons import *",
            "from ID_animations import *",
        ]

    header_lines: List[str] = [
        "# -*- coding: cp1252 -*-",
        "# AUTO-GENERATED by build/build_scripts.py (do not edit by hand)",
        *preamble,
        "",
    ]
    header_lines += build_index(all_files)
    if fragment_preamble_lines:
        header_lines += fragment_preamble_lines
    header_lines += [
        "scripts = [",
        "",
    ]

    entries: List[str] = []
    prev_top = prev_sub = None

    for fp in all_files:
        rel = fp.relative_to(SRC)
        rel_parts = list(rel.parts[:-1])
        top_code, top_label, sub_code, sub_label = parse_codes_from_path(rel_parts)

        # Section banners (searchable by ZH, ZH06, etc.)
        if top_code and top_code != prev_top:
            entries.append("")
            entries.append("#" + ("=" * 118))
            entries.append(f"# _{top_code}_ - {_prettify(top_label or '')}".rstrip())
            entries.append("#" + ("=" * 118))
            prev_top = top_code
            prev_sub = None

        if sub_code and sub_code != prev_sub:
            entries.append(f"# [ {sub_code} ] - {_prettify(sub_label or '')}".rstrip())
            prev_sub = sub_code

        raw = fp.read_text(encoding="utf-8", errors="replace")
        if "SCRIPTS" not in raw:
            continue

        inner, base_line = extract_list_block_span(raw, "SCRIPTS")

        rel_posix = (SRC / rel).relative_to(ROOT).as_posix()
        chunks = _split_script_entries(inner, base_line)

        # If we couldn't split, fall back to a single fragment-level marker.
        if not chunks:
            block = inner.rstrip()
            if block.strip():
                if not block.rstrip().endswith(","):
                    block += ","
                if emit_source_map:
                    entries.append(f"# [ {rel_posix} ]")
                entries.append(block)
            continue

        for chunk_text, s_line, e_line, sid in chunks:
            if not chunk_text.strip():
                continue
            if emit_source_map:
                entries.append(f"# [ {rel_posix}:L{s_line}-L{e_line} ] {sid}")
            entries.append(chunk_text)

    out_lines = header_lines + entries + ["]", "SCRIPTS = scripts", ""]
    OUT.write_text("\n".join(out_lines), encoding="cp1252", errors="replace")

    if use_cache:
        preamble_files: List[Path] = []
        if PREAMBLE_DIR.exists():
            preamble_files = [p for p in PREAMBLE_DIR.glob("*.py") if p.is_file()]
            preamble_files.sort(key=lambda p: p.name.lower())

        za_sig = _sig_for(ZA_ORDER_FILE) if ZA_ORDER_FILE.exists() else None

        payload = {
            "schema": CACHE_SCHEMA_VERSION,
            "builder_sha256": _builder_fingerprint(),
            "emit_source_map": bool(emit_source_map),
            "fragments": [_sig_for(p) for p in all_files],
            "preamble": [_sig_for(p) for p in preamble_files],
            "za_order": za_sig,
        }
        _write_cache(payload)

    print(f"[build_scripts] Wrote {OUT}")


if __name__ == "__main__":
    from build_profile import parse_profile, emit_source_map
    prof = parse_profile()
    build(emit_source_map=emit_source_map(prof))
