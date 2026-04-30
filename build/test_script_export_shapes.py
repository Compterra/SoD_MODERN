# -*- coding: utf-8 -*-
from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _name_targets_function(name: str, assignments: dict[str, ast.AST], functions: set[str]) -> bool:
    if name in functions:
        return True
    value = assignments.get(name)
    return isinstance(value, ast.Name) and value.id in functions


def main() -> None:
    failures: list[str] = []
    for path in (ROOT / "src" / "scripts").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        functions = {
            node.name
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        assignments: dict[str, ast.AST] = {}
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assignments[target.id] = node.value

        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            if not any(isinstance(target, ast.Name) and target.id == "SCRIPTS" for target in node.targets):
                continue
            if not isinstance(node.value, (ast.List, ast.Tuple)):
                continue
            for script_entry in node.value.elts:
                if not isinstance(script_entry, (ast.List, ast.Tuple)) or len(script_entry.elts) < 2:
                    continue
                operations = script_entry.elts[1]
                if isinstance(operations, ast.Name) and _name_targets_function(
                    operations.id, assignments, functions
                ):
                    failures.append(f"{path.relative_to(ROOT)} exports callable {operations.id!r} in SCRIPTS")

    if failures:
        raise AssertionError("\n".join(failures))
    print("test_script_export_shapes: OK")


if __name__ == "__main__":
    main()
