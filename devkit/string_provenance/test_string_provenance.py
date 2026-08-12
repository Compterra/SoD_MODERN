#!/usr/bin/env python3
"""Fixture and workspace checks for interprocedural string provenance."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devkit.string_integrity import string_integrity as integrity
from devkit.string_provenance import string_provenance as provenance


RAW = """
scripts = [
  ('root', [
    (call_script, script_middle),
  ]),
  ('middle', [
    (try_begin),
      (eq, ':mode', 1),
      (call_script, script_writer),
    (else_try),
      (str_store_string, s68, '@alternate'),
    (try_end),
  ]),
  ('writer', [
    (str_store_string, s68, '@writer'),
    (str_store_string_reg, s69, s68),
  ]),
]
"""


def fixture_index() -> provenance.StringProvenanceIndex:
    module = integrity.ModuleData(
        path=Path("fixture/module_scripts.py"),
        relative_path="compile/module_scripts.py",
        raw=RAW,
        tree=ast.parse(RAW),
        marker_lines=[],
        markers=[],
    )
    scripts = provenance.build_script_records(module)

    class Ledger:
        export_index = {}

    return provenance.StringProvenanceIndex(ROOT, module, Ledger(), scripts, {}, [])  # type: ignore[arg-type]


def test_nested_paths_and_branches() -> None:
    index = fixture_index()
    summary = provenance.script_writer_paths(index, "script_root", "s68")
    assert len(summary.paths) == 2
    chains = {tuple(path.call_chain) for path in summary.paths}
    assert ("script_root", "script_middle", "script_writer") in chains
    assert ("script_root", "script_middle") in chains
    nested = next(path for path in summary.paths if path.call_chain[-1] == "script_writer")
    assert any(condition.name == "eq" for condition in nested.conditions)
    copied = provenance.script_writer_paths(index, "script_writer", "s69")
    assert copied.paths[0].source_register == "s68"


def test_workspace_index() -> None:
    index = provenance.build_string_provenance(ROOT)
    summary = provenance.summary_payload(index, limit=3)
    assert summary["coverage"]["script_count"] > 1_000
    assert summary["coverage"]["direct_string_writer_count"] > 0


def main() -> int:
    test_nested_paths_and_branches()
    test_workspace_index()
    print("[string_provenance] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
