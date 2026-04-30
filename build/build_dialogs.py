# -*- coding: utf-8 -*-
"""
Build compile/module_dialogs.py from src/dialogs fragments (vanilla-compatible).

Dialogs are STRICTLY ordered. The dialog system scans lines top-to-bottom.
We preserve order using src/dialogs/_order_dialogs.txt which lists fragment paths
(relative to src/dialogs).
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional
import re
import ast
import io
import tokenize

import json
import hashlib
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "dialogs"
OUT = ROOT / "compile" / "module_dialogs.py"

# Incremental build cache (v42): skip regeneration if inputs unchanged
CACHE_SCHEMA_VERSION = 1
CACHE_DIR = ROOT / ".buildcache"
CACHE_FILE = CACHE_DIR / "dialogs_manifest.json"


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
ORDER_FILE = SRC / "_order_dialogs.txt"

DOCS_DIR = ROOT / "docs"
DOCS_EDIT = DOCS_DIR / "edit"
DOCS_REPORTS = DOCS_DIR / "reports"
ALLOWLIST_PATH = DOCS_EDIT / "dialog_head_allowlist.txt"
DUPE_REPORT_PATH = DOCS_REPORTS / "dialog_head_duplicates.txt"


# Optional: user-defined preamble lines live here.
# If present, they replace the hardcoded import block below.
PREAMBLE_DIR = SRC / "_preamble"

def _line_no(raw: str, idx: int) -> int:
    return raw.count("\n", 0, idx) + 1


def _check_dialog_string_newlines(fp: Path, raw: str, inner: str, start_ln: int) -> None:
    """
    Warband's dialog text exporter/load path is not safe for embedded newlines.
    Catch both explicit escapes (\\n/\\r) and newline-bearing triple quoted text.
    """
    reader = io.StringIO(inner).readline
    try:
        tokens = tokenize.generate_tokens(reader)
        for tok in tokens:
            if tok.type != tokenize.STRING:
                continue
            try:
                value = ast.literal_eval(tok.string)
            except Exception:
                continue
            if not isinstance(value, str):
                continue
            if "\n" not in value and "\r" not in value:
                continue
            line = start_ln + tok.start[0] - 1
            col = tok.start[1] + 1
            rel = fp.relative_to(ROOT).as_posix()
            preview = value.replace("\r", "\\r").replace("\n", "\\n")
            if len(preview) > 120:
                preview = preview[:117] + "..."
            raise SystemExit(
                f"[build_dialogs] FAIL: {rel}:{line}:{col} dialog string contains newline escape(s): {preview}"
            )
    except tokenize.TokenError as e:
        rel = fp.relative_to(ROOT).as_posix()
        raise SystemExit(f"[build_dialogs] FAIL: {rel}:{start_ln}: tokenization failed while checking dialog strings: {e}")


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

def read_order() -> List[Path]:
    if not ORDER_FILE.exists():
        raise SystemExit(f"Missing dialogs order file: {ORDER_FILE}")
    files: List[Path] = []
    for ln in ORDER_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        # allow 'CODE<TAB>relative/path.py' format; take last token
        parts = ln.split()
        rel = parts[-1].replace("\\", "/")
        p = SRC / rel
        if not p.exists():
            raise SystemExit(f"Dialog fragment listed but missing: {p}")
        files.append(p)
    return files

def extract_dialog_route_key(inner: str) -> str:
    """
    Best-effort dialog route key:
    speaker_token::input_state->output_state

    This is intentionally conservative. We want duplicate reporting to cluster
    likely copy-paste collisions, not every common first condition in the tree.
    """
    m = re.search(
        r'^\s*\[\s*([^,\]]+)\s*,\s*"([^"]+)"\s*,\s*\[(.*?)\]\s*,\s*"((?:[^"\\]|\\.)*)"\s*,\s*"([^"]+)"',
        inner,
        re.S,
    )
    if not m:
        return ""
    speaker = m.group(1).strip()
    input_state = m.group(2).strip()
    output_state = m.group(5).strip()
    return f"{speaker}::{input_state}->{output_state}"


def extract_dialog_head_signature(inner: str, max_ops: int = 3) -> str:
    """
    Summarize the first few head operations from the condition list.

    Using the route key plus a short head-op chain is much less noisy than
    grouping every dialog that happens to start with the same first opcode.
    """
    m = re.search(
        r'^\s*\[\s*([^,\]]+)\s*,\s*"([^"]+)"\s*,\s*\[(.*?)\]\s*,\s*"((?:[^"\\]|\\.)*)"\s*,\s*"([^"]+)"',
        inner,
        re.S,
    )
    if not m:
        return ""
    head = m.group(3)
    ops = [mm.group(1).strip() for mm in re.finditer(r'\(\s*([A-Za-z0-9_|]+)', head)]
    if not ops:
        return "no_conditions"
    return "|".join(ops[:max_ops])


def extract_dialog_text_fingerprint(inner: str) -> str:
    """
    Small normalized text fingerprint so repeated route/options only cluster when
    they also look like the same player-facing line.
    """
    m = re.search(
        r'^\s*\[\s*([^,\]]+)\s*,\s*"([^"]+)"\s*,\s*\[(.*?)\]\s*,\s*"((?:[^"\\]|\\.)*)"\s*,\s*"([^"]+)"',
        inner,
        re.S,
    )
    if not m:
        return ""
    text = m.group(4)
    text = text.replace("\\\n", " ")
    text = re.sub(r"\{[^}]+\}", "{var}", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    if not text:
        return "empty_text"
    if len(text) > 64:
        text = text[:64]
    return text

def load_preamble_lines() -> List[str]:
    """Load preamble lines from src/dialogs/_preamble/*.py, if any."""
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


def _load_allowlist_patterns(path: Path) -> List[re.Pattern]:
    """Load wildcard patterns (with '*') from docs/dialog_head_allowlist.txt."""
    if not path.exists():
        return []
    pats: List[re.Pattern] = []
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        expr = re.escape(ln.lower()).replace(r"\*", ".*")
        pats.append(re.compile(rf"^{expr}$", re.IGNORECASE))
    return pats


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
    allowlist_sig = _sig_for(ALLOWLIST_PATH) if ALLOWLIST_PATH.exists() else None
    cache_payload = {
        'schema': CACHE_SCHEMA_VERSION,
        'builder_sha256': _builder_fingerprint(),
        'emit_source_map': bool(emit_source_map),
        'fragments': [_sig_for(p) for p in files],
        'preamble': [_sig_for(p) for p in preamble_files],
        'order_file': order_sig,
        'allowlist_sig': allowlist_sig,
    }
    if use_cache and OUT.exists():
        prev = _load_cache()
        if prev == cache_payload:
            print('[build_dialogs] Up-to-date; skipped (cache)')
            return

    DOCS_REPORTS.mkdir(parents=True, exist_ok=True)
    DOCS_EDIT.mkdir(parents=True, exist_ok=True)
    allow = _load_allowlist_patterns(ALLOWLIST_PATH)

    def is_allowlisted(sig: str) -> bool:
        if not allow:
            # Reasonable default: ignore signatures that clearly reference globals.
            # These are very common and not helpful to spam about.
            return "$" in sig
        s = sig.lower()
        return any(p.match(s) for p in allow)

    # Duplicate-ish detection: group likely copy-paste collisions by dialog route
    # and a short normalized head-op chain instead of a single common opcode.
    seen: Dict[str, Path] = {}
    dups: Dict[str, List[Path]] = {}
    entries: List[str] = []

    for fp in files:
        raw = fp.read_text(encoding="utf-8", errors="replace")
        _syntax_check_fragment(fp, raw)
        if "DIALOGS" not in raw:
            continue
        inner, start_ln, end_ln = extract_list_block(raw, "DIALOGS")
        _check_dialog_string_newlines(fp, raw, inner, start_ln)
        route_key = extract_dialog_route_key(inner)
        head_sig = extract_dialog_head_signature(inner)
        text_sig = extract_dialog_text_fingerprint(inner)
        sig = f"{route_key} [{head_sig}] {{{text_sig}}}" if route_key and head_sig and text_sig else ""
        if sig:
            if sig in seen:
                # Collect duplicates; we'll report a compact summary at the end.
                if not is_allowlisted(sig):
                    dups.setdefault(sig, [seen[sig]]).append(fp)
            else:
                seen[sig] = fp
        block = inner.rstrip()
        if block and not block.rstrip().endswith(","):
            block += ","
        rel = fp.relative_to(SRC).as_posix()
        label = f"# [ src/dialogs/{rel}:L{start_ln}-L{end_ln} ]"
        if sig:
            label += f" {sig}"
        if emit_source_map:
            entries.append(label)
        entries.append(block)

    # Write a compact duplicate summary (optional) to reduce console noise.
    if dups:
        # Stable ordering: most repeated first.
        items = sorted(dups.items(), key=lambda kv: (-len(kv[1]), kv[0].lower()))
        # Console: show only a few lines.
        max_console = 10
        shown = 0
        for sig, paths in items:
            if shown >= max_console:
                break
            print(
                f"[build_dialogs] NOTE: duplicate dialog head '{sig}' ({len(paths)} fragments); "
                f"first: {paths[0]}"
            )
            shown += 1
        if len(items) > max_console:
            print(f"[build_dialogs] NOTE: ...and {len(items) - max_console} more duplicate head signature(s) (see {DUPE_REPORT_PATH}).")

        # Full report file for later review.
        lines: List[str] = []
        lines.append("Dialog head duplicates (heuristic)")
        lines.append("")
        lines.append(f"Total duplicate signatures: {len(items)}")
        lines.append("")
        for sig, paths in items:
            lines.append(f"- {sig}  ({len(paths)} fragments)")
            for p in paths:
                lines.append(f"    {p.relative_to(ROOT).as_posix()}")
            lines.append("")
        DUPE_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", errors="replace")
    else:
        # Keep the report file from going stale between builds.
        DUPE_REPORT_PATH.write_text(
            "Dialog head duplicates (heuristic)\n\nNo non-allowlisted duplicates detected.\n",
            encoding="utf-8",
            errors="replace",
        )


    preamble = load_preamble_lines()
    if not preamble:
        # Fallback (legacy) preamble.
        preamble = [
            'from header_common import *',
            'from header_dialogs import *',
            'from header_operations import *',
            'from header_parties import *',
            'from header_item_modifiers import *',
            'from header_skills import *',
            'from header_triggers import *',
            'from ID_troops import *',
            'from ID_party_templates import *',
            'from module_constants import *',
        ]

    header_lines: List[str] = [
        '# -*- coding: cp1252 -*-',
        '# AUTO-GENERATED by build/build_dialogs.py (do not edit by hand)',
        *preamble,
        '',
        'dialogs = [',
        '',
    ]
    out_lines = header_lines + entries + ["]", ""]
    OUT.write_text("\n".join(out_lines), encoding="cp1252", errors="replace")

    if use_cache:
        _write_cache(cache_payload)
    print(f"[build_dialogs] Wrote {OUT}")

def _syntax_check_fragment(fp: Path, raw: str) -> None:
    """Fast-fail syntax check with precise file/line reporting."""
    try:
        compile(raw, fp.as_posix(), 'exec')
    except SyntaxError as e:
        lines = raw.splitlines()
        lineno = int(getattr(e, 'lineno', 0) or 0)
        offset = int(getattr(e, 'offset', 0) or 0)
        msg = getattr(e, 'msg', 'SyntaxError')
        start = max(1, lineno - 2)
        end = min(len(lines), lineno + 2)
        snippet = []
        for i in range(start, end + 1):
            mark = '>' if i == lineno else ' '
            snippet.append(f"{mark}{i:4d}| {lines[i-1]}")
        sn = '\n'.join(snippet)
        rel = fp.relative_to(Path(__file__).resolve().parents[1]).as_posix()
        raise SystemExit(f"[build_dialogs] FAIL: {rel}:{lineno}:{offset} {msg}\n{sn}")


if __name__ == "__main__":
    from build_profile import parse_profile, emit_source_map
    prof = parse_profile()
    build(emit_source_map=emit_source_map(prof))
