# -*- coding: utf-8 -*-
"""
Build compile/module_quests.py from src/quests fragments.

Why this exists:
- Quests were still maintained in legacy compile/module_quests.py.
- This builder makes quests source-driven like the other modular domains.
- The Warband compiler still receives the same final `quests = [...]` structure.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "quests"
OUT = ROOT / "compile" / "module_quests.py"

PREAMBLE_DIR = SRC / "_preamble"
ORDER_FILE = SRC / "_order_quests.txt"


def _find_assignment_start(raw: str, var_name: str) -> int:
    match = re.search(rf"(?m)^[ \t]*{re.escape(var_name)}\s*=", raw)
    if match is None:
        raise ValueError(f"Missing {var_name} assignment in fragment.")
    return match.start()


def _has_assignment(raw: str, var_name: str) -> bool:
    return re.search(rf"(?m)^[ \t]*{re.escape(var_name)}\s*=", raw) is not None


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
            snippet.append(f"{prefix}{i:4d}| {lines[i - 1]}")
        sn = "\n".join(snippet)

        rel = fp.relative_to(ROOT).as_posix() if fp.is_absolute() else fp.as_posix()
        raise SystemExit(f"[build_quests] FAIL: {rel}:{lineno}:{offset} {msg}\n{sn}")


def extract_list_block_span(raw: str, var_name: str) -> Tuple[str, int]:
    """
    Return (inner_text, base_line) for: VAR = [ ... ]

    - inner_text is the exact substring between '[' and the matching ']'
    - base_line is the 1-based line number containing the '['
    """
    idx = _find_assignment_start(raw, var_name)
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


def extract_prefix_before_var(raw: str, var_name: str) -> str:
    idx = _find_assignment_start(raw, var_name)
    return raw[:idx].rstrip()


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


def order_files_folder_driven() -> List[Path]:
    all_files = [
        p
        for p in SRC.rglob("*.py")
        if p.is_file() and "_preamble" not in p.parts
    ]
    all_files.sort(key=lambda p: p.relative_to(SRC).as_posix().lower())
    return all_files


def apply_order(all_files: List[Path]) -> List[Path]:
    if not ORDER_FILE.exists():
        return all_files

    rel_to_src = {str(p.relative_to(SRC)).replace("\\", "/"): p for p in all_files}

    ordered: List[Path] = []
    for rel in read_order_list(ORDER_FILE):
        p = rel_to_src.get(rel)
        if p:
            ordered.append(p)

    listed = set(ordered)
    ordered += [p for p in all_files if p not in listed]
    return ordered


def load_preamble_lines() -> List[str]:
    if not PREAMBLE_DIR.exists():
        return []

    files = [p for p in PREAMBLE_DIR.glob("*.py") if p.is_file()]
    files.sort(key=lambda p: p.name.lower())

    lines: List[str] = []
    for fp in files:
        raw = fp.read_text(encoding="utf-8", errors="replace").splitlines()
        for ln in raw:
            ln = ln.rstrip()
            if ln:
                lines.append(ln)
    return lines


def _split_quest_entries(inner: str, base_line: int) -> List[Tuple[str, int, int, str]]:
    """
    Split inner QUESTS list content into per-quest chunks.

    Returns:
      (chunk_text, start_line, end_line, quest_id)
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

    for idx, (s_i, qid) in enumerate(starts):
        e_i = (starts[idx + 1][0] - 1) if (idx + 1) < len(starts) else (len(lines) - 1)

        while e_i > s_i and lines[e_i].strip() == "":
            e_i -= 1

        chunk_lines = lines[s_i : e_i + 1]

        k = len(chunk_lines) - 1
        while k >= 0 and chunk_lines[k].strip() == "":
            k -= 1
        if k >= 0 and not chunk_lines[k].rstrip().endswith(","):
            chunk_lines[k] = chunk_lines[k].rstrip() + ","

        chunk_text = "\n".join(chunk_lines).rstrip()
        start_line = base_line + s_i
        end_line = base_line + e_i
        chunks.append((chunk_text, start_line, end_line, qid))

    return chunks


def _collect_duplicate_quest_ids(all_files: List[Path]) -> Optional[str]:
    seen: Dict[str, Path] = {}
    rx = re.compile(r'^\s*\(\s*"([^"]+)"\s*,', re.MULTILINE)

    for fp in all_files:
        raw = fp.read_text(encoding="utf-8", errors="replace")
        _syntax_check_fragment(fp, raw)

        if not _has_assignment(raw, "QUESTS"):
            continue

        inner, _ = extract_list_block_span(raw, "QUESTS")
        for match in rx.finditer(inner):
            qid = match.group(1)
            if qid in seen:
                first = seen[qid].relative_to(ROOT).as_posix()
                second = fp.relative_to(ROOT).as_posix()
                return f"Duplicate quest id '{qid}':\n  {first}\n  {second}"
            seen[qid] = fp

    return None


def build(use_cache: bool = True, emit_source_map: bool = True) -> None:
    del use_cache  # quests are small; keep this builder simple and deterministic

    if not SRC.exists():
        raise SystemExit(f"Missing source folder: {SRC}")

    all_files = apply_order(order_files_folder_driven())

    duplicate_error = _collect_duplicate_quest_ids(all_files)
    if duplicate_error:
        raise SystemExit(f"[build_quests] FAIL: {duplicate_error}")

    preamble = load_preamble_lines()
    if not preamble:
        preamble = ["from header_quests import *"]

    header_lines: List[str] = [
        "# -*- coding: cp1252 -*-",
        "# AUTO-GENERATED by build/build_quests.py (do not edit by hand)",
        *preamble,
        "",
    ]

    setup_lines: List[str] = []
    entries: List[str] = []

    for fp in all_files:
        raw = fp.read_text(encoding="utf-8", errors="replace")
        if not _has_assignment(raw, "QUESTS"):
            continue

        rel_posix = fp.relative_to(ROOT).as_posix()
        prefix = extract_prefix_before_var(raw, "QUESTS")
        if prefix.strip():
            if emit_source_map:
                setup_lines.append(f"# [ {rel_posix} ]")
            setup_lines.append(prefix)
            setup_lines.append("")

        inner, base_line = extract_list_block_span(raw, "QUESTS")
        chunks = _split_quest_entries(inner, base_line)

        if not chunks:
            block = inner.rstrip()
            if block.strip():
                if not block.rstrip().endswith(","):
                    block += ","
                if emit_source_map:
                    entries.append(f"# [ {rel_posix} ]")
                entries.append(block)
                entries.append("")
            continue

        if emit_source_map:
            entries.append(f"# --- {fp.relative_to(SRC).as_posix()} ---")

        for chunk_text, s_line, e_line, qid in chunks:
            if not chunk_text.strip():
                continue
            if emit_source_map:
                entries.append(f"# [ {rel_posix}:L{s_line}-L{e_line} ] {qid}")
            entries.append(chunk_text)

        entries.append("")

    out_lines = header_lines + setup_lines + ["quests = [", ""] + entries + ["]", ""]
    OUT.write_text("\n".join(out_lines), encoding="cp1252", errors="replace")
    print(f"[build_quests] Wrote {OUT}")


if __name__ == "__main__":
    from build_profile import emit_source_map, parse_profile

    prof = parse_profile()
    build(emit_source_map=emit_source_map(prof))
