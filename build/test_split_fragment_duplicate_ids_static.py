from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))

import build_presentations  # noqa: E402
import build_scripts  # noqa: E402


def test_src_scripts_export_unique_script_ids() -> None:
    seen: dict[str, Path] = {}
    duplicates: dict[str, list[Path]] = defaultdict(list)

    files = build_scripts.apply_za_order(build_scripts.order_files_folder_driven())
    for fp in files:
        raw = fp.read_text(encoding="utf-8", errors="replace")
        if "SCRIPTS" not in raw:
            continue
        inner, base_line = build_scripts.extract_list_block_span(raw, "SCRIPTS")
        script_ids = [script_id for _chunk, _start, _end, script_id in build_scripts._split_script_entries(inner, base_line)]
        if not script_ids:
            first = build_scripts.extract_script_name_from_fragment(raw)
            script_ids = [first] if first else []
        for script_id in script_ids:
            if script_id in seen:
                duplicates[script_id].append(fp.relative_to(ROOT))
            else:
                seen[script_id] = fp.relative_to(ROOT)

    assert not duplicates, {
        script_id: [str(seen[script_id]), *map(str, paths)]
        for script_id, paths in sorted(duplicates.items())
    }


def test_src_presentations_export_unique_presentation_ids() -> None:
    seen: dict[str, Path] = {}
    duplicates: dict[str, list[Path]] = defaultdict(list)

    for fp in build_presentations.read_order():
        raw = fp.read_text(encoding="utf-8", errors="replace")
        if "PRESENTATIONS" not in raw:
            continue
        inner, _start_line, _end_line = build_presentations.extract_list_block(raw, "PRESENTATIONS")
        for presentation_id in build_presentations.extract_ids(inner):
            if presentation_id in seen:
                duplicates[presentation_id].append(fp.relative_to(ROOT))
            else:
                seen[presentation_id] = fp.relative_to(ROOT)

    assert not duplicates, {
        presentation_id: [str(seen[presentation_id]), *map(str, paths)]
        for presentation_id, paths in sorted(duplicates.items())
    }


def test_builders_check_all_split_fragment_ids_not_only_first_id() -> None:
    scripts_builder = (ROOT / "build" / "build_scripts.py").read_text(encoding="utf-8")
    presentations_builder = (ROOT / "build" / "build_presentations.py").read_text(encoding="utf-8")

    assert "Check every" in scripts_builder
    assert "for _chunk_text, s_line, _e_line, script_id in chunks" in scripts_builder
    assert "def extract_ids" in presentations_builder
    assert "for pid in ids" in presentations_builder


def test_script_builder_strips_legacy_import_shim_after_comments() -> None:
    raw = """# COST: documented preamble
try:
    from src.compiler import *
except ImportError:
    from src.module_system import *

from src.constants.module_constants import *

SCRIPTS = [
("sample", []),
]
"""
    preamble = build_scripts.extract_fragment_preamble_block(raw)

    assert "# COST: documented preamble" in preamble
    assert "from src.constants.module_constants import *" in preamble
    assert "src.compiler" not in preamble
    assert "src.module_system" not in preamble


def test_generated_scripts_do_not_embed_legacy_src_import_shims() -> None:
    generated = (ROOT / "compile" / "module_scripts.py").read_text(encoding="utf-8", errors="replace")

    assert "from src.compiler import *" not in generated
    assert "from src.module_system import *" not in generated


if __name__ == "__main__":
    test_src_scripts_export_unique_script_ids()
    test_src_presentations_export_unique_presentation_ids()
    test_builders_check_all_split_fragment_ids_not_only_first_id()
    test_script_builder_strips_legacy_import_shim_after_comments()
    test_generated_scripts_do_not_embed_legacy_src_import_shims()
    print("test_split_fragment_duplicate_ids_static: OK")
