# -*- coding: utf-8 -*-
"""
Build compile/module_presentations.py from src/presentations fragments (vanilla-compatible).

Policy:
- Strict manifest ordering via src/presentations/_order_presentations.txt.
- One presentation per fragment file, exporting PRESENTATIONS = [ (...), ].
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional
import re

import json
import hashlib
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "presentations"
OUT = ROOT / "compile" / "module_presentations.py"

# Incremental build cache (v42): skip regeneration if inputs unchanged
CACHE_SCHEMA_VERSION = 1
CACHE_DIR = ROOT / ".buildcache"
CACHE_FILE = CACHE_DIR / "presentations_manifest.json"


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _builder_fingerprint() -> str:
    # Invalidate cache when this builder changes
    return _sha256_file(Path(__file__).resolve())


def _sig_for(path: Path) -> dict:
    st = path.stat()
    return {
        "rel": path.relative_to(ROOT).as_posix(),
        "mtime_ns": int(getattr(st, "st_mtime_ns", int(st.st_mtime * 1e9))),
        "size": int(st.st_size),
    }


def _load_cache() -> 'Optional[dict]':
    if not CACHE_FILE.exists():
        return None
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def _write_cache(payload: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


# Optional: user-defined preamble lines live here.
# If present, they replace the hardcoded import block below.
PREAMBLE_DIR = SRC / "_preamble"
ORDER_FILE = SRC / "_order_presentations.txt"
def _line_no(raw: str, idx: int) -> int:
    return raw.count("\n", 0, idx) + 1


def _syntax_check_fragment(fp: Path, raw: str) -> None:
    try:
        compile(raw, fp.as_posix(), "exec")
    except SyntaxError as e:
        lines = raw.splitlines()
        lineno = int(getattr(e, "lineno", 0) or 0)
        offset = int(getattr(e, "offset", 0) or 0)
        msg = getattr(e, "msg", "SyntaxError")
        start = max(1, lineno - 2)
        end = min(len(lines), lineno + 2)
        snippet = []
        for i in range(start, end + 1):
            prefix = ">" if i == lineno else " "
            snippet.append(f"{prefix}{i:4d}| {lines[i-1]}")
        rel = fp.relative_to(ROOT).as_posix() if fp.is_absolute() else fp.as_posix()
        raise SystemExit(f"[build_presentations] FAIL: {rel}:{lineno}:{offset} {msg}\n" + "\n".join(snippet))


def extract_list_block(raw: str, var_name: str) -> tuple[str, int, int]:
    """
    Return (inner_text, start_line, end_line) of: VAR = [ ... ]  (handles strings + # comments)
    Raises ValueError if not found or unclosed.
    """
    idx = raw.find(var_name)
    if idx < 0:
        raise ValueError(f"Missing {var_name} in fragment.")
    lb = raw.find("[", idx)
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

        # not in string/comment
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
                start_ln = _line_no(raw, lb)
                end_ln = _line_no(raw, i)
                return raw[lb + 1 : i].strip(), start_ln, end_ln
        i += 1

    raise ValueError(f"Unclosed list bracket for {var_name}.")

def extract_ids(raw: str) -> List[str]:
    # Match each presentation tuple opening: ("id",
    return [
        match.group(1)
        for match in re.finditer(r'^\s*\(\s*"([^"]+)"\s*,', raw, re.MULTILINE)
    ]


def load_preamble_lines() -> List[str]:
    """Load preamble lines from src/presentations/_preamble/*.py, if any."""
    if not PREAMBLE_DIR.exists():
        return []

    files = [p for p in PREAMBLE_DIR.glob('*.py') if p.is_file()]
    files.sort(key=lambda p: p.name.lower())

    lines: List[str] = []
    for fp in files:
        for ln in fp.read_text(encoding='utf-8', errors='replace').splitlines():
            ln = ln.rstrip()
            if ln:
                lines.append(ln)
    return lines


def read_order() -> List[Path]:
    if not ORDER_FILE.exists():
        raise SystemExit(f"Missing presentations order file: {ORDER_FILE}")
    files: List[Path] = []
    seen: set[str] = set()
    for ln in ORDER_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        rel = ln.replace("\\", "/")
        if rel in seen:
            raise SystemExit(f"Duplicate entry in presentations order file: {rel}")
        seen.add(rel)
        p = SRC / rel
        if not p.exists():
            raise SystemExit(f"Presentation fragment listed but missing: {p}")
        files.append(p)
    return files

def build(use_cache: bool = True, emit_source_map: bool = True) -> None:
    if not SRC.exists():
        raise SystemExit(f"Missing source folder: {SRC}")

    files = read_order()

    # Incremental cache: compare inputs and skip regeneration when unchanged
    preamble_files: List[Path] = []
    if PREAMBLE_DIR.exists():
        preamble_files = [p for p in PREAMBLE_DIR.glob('*.py') if p.is_file()]
        preamble_files.sort(key=lambda p: p.name.lower())
    order_sig = _sig_for(ORDER_FILE) if ORDER_FILE.exists() else None
    cache_payload = {
        'schema': CACHE_SCHEMA_VERSION,
        'builder_sha256': _builder_fingerprint(),
        'emit_source_map': bool(emit_source_map),
        'fragments': [_sig_for(p) for p in files],
        'preamble': [_sig_for(p) for p in preamble_files],
        'order_file': order_sig,
    }
    if use_cache and OUT.exists():
        prev = _load_cache()
        if prev == cache_payload:
            print('[build_presentations] Up-to-date; skipped (cache)')
            return

    # Duplicate detection
    seen: Dict[str, Path] = {}
    entries: List[str] = []

    for fp in files:
        raw = fp.read_text(encoding="utf-8", errors="replace")
        _syntax_check_fragment(fp, raw)
        if "PRESENTATIONS" not in raw:
            continue
        inner, start_ln, end_ln = extract_list_block(raw, "PRESENTATIONS")
        ids = extract_ids(inner)
        for pid in ids:
            if pid in seen:
                raise SystemExit(f"Duplicate presentation '{pid}':\n  {seen[pid]}\n  {fp}")
            seen[pid] = fp
        pid = ids[0] if ids else ""
        block = inner.rstrip()
        if block and not block.rstrip().endswith(","):
            block += ","
        rel = fp.relative_to(SRC).as_posix()
        label = f"# [ src/presentations/{rel}:L{start_ln}-L{end_ln} ]"
        if pid:
            label += f" {pid}"
        if emit_source_map:
            entries.append(label)
        entries.append(block)

    preamble = load_preamble_lines()
    if not preamble:
        # Fallback (legacy) preamble.
        preamble = [
            'from header_common import *',
            'from header_presentations import *',
            'from header_mission_templates import *',
            'from ID_meshes import *',
            'from header_operations import *',
            'from header_triggers import *',
            'from module_constants import *',
            'import string',
        ]

    header_lines: List[str] = [
        '# -*- coding: cp1252 -*-',
        '# AUTO-GENERATED by build/build_presentations.py (do not edit by hand)',
        *preamble,
        '',
        'presentations = [',
        '',
    ]

    out_lines = header_lines + entries + [']', '']
    OUT.write_text("\n".join(out_lines), encoding="cp1252", errors="replace")

    if use_cache:
        _write_cache(cache_payload)
    print(f"[build_presentations] Wrote {OUT}")

if __name__ == "__main__":
    from build_profile import parse_profile, emit_source_map
    prof = parse_profile()
    build(emit_source_map=emit_source_map(prof))
