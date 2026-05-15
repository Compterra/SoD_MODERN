from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "scripts" / "ZD_centers" / "print_troop_owned_centers_in_numbers_to_s0.py"


def _name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    return None


def test_fief_list_helper_does_not_self_reference_s0_while_writing_s0() -> None:
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8", errors="replace"))
    offenders: list[int] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Tuple, ast.List)) or len(node.elts) < 3:
            continue
        if _name(node.elts[0]) != "str_store_string":
            continue
        if _name(node.elts[1]) != "s0":
            continue
        source = node.elts[2]
        if isinstance(source, ast.Constant) and isinstance(source.value, str):
            if "{s0}" in source.value:
                offenders.append(node.lineno)

    assert not offenders, (
        "print_troop_owned_centers_in_numbers_to_s0 should copy s0 to "
        f"a scratch register before composing with it; offending line(s): {offenders}"
    )
