# -*- coding: utf-8 -*-
"""Helpers for modular constants merging."""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
SRC_CONSTANTS = ROOT / "src" / "constants"
ORDER_FILE = SRC_CONSTANTS / "_order_constants.txt"


def load_order_entries() -> List[str]:
    if not ORDER_FILE.exists():
        return []
    entries: List[str] = []
    for line in ORDER_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        entries.append(line)
    return entries


def ordered_constant_py_files(src_dir: Path = SRC_CONSTANTS) -> List[Path]:
    if not src_dir.exists():
        return []
    by_name = {
        p.name: p
        for p in src_dir.glob("*.py")
        if p.is_file() and not p.name.startswith("_")
    }
    ordered: List[Path] = []
    seen: set[str] = set()
    for entry in load_order_entries():
        name = entry if entry.endswith(".py") else f"{entry}.py"
        if name not in by_name:
            raise SystemExit(f"[constants_merge] Order file lists missing constants module: {name}")
        ordered.append(by_name[name])
        seen.add(name)
    for name in sorted(by_name.keys()):
        if name not in seen:
            ordered.append(by_name[name])
    return ordered


def extract_top_level_assignments(path: Path) -> Dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    tree = ast.parse(text, filename=str(path))

    def value_src(node: ast.expr) -> str:
        if hasattr(ast, "unparse"):
            return ast.unparse(node).strip()
        return ast.dump(node)

    out: Dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    out[target.id] = value_src(node.value)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
            out[node.target.id] = value_src(node.value)
    return out


def find_duplicate_names_across_files(files: List[Path]) -> List[Tuple[str, Path, Path]]:
    owner: Dict[str, Path] = {}
    dups: List[Tuple[str, Path, Path]] = []
    for fp in files:
        for name in extract_top_level_assignments(fp).keys():
            if name in owner:
                dups.append((name, owner[name], fp))
            else:
                owner[name] = fp
    return dups
