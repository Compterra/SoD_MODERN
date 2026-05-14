# -*- coding: utf-8 -*-
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "build" / "dialogue_immersion_report.py"


def load_report_module():
    spec = importlib.util.spec_from_file_location("dialogue_immersion_report", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_dialogue_immersion_report_covers_core_states_and_categories() -> None:
    module = load_report_module()
    entries = module.iter_entries()
    states = {state for _path, _speaker, state in entries}
    categories = {module.classify(ROOT / path) for path, _speaker, _state in entries}
    rendered = module.render()

    assert len(entries) > 1000
    for state in [
        "start",
        "lord_start",
        "member_chat",
        "mayor_pretalk",
        "mayor_friendly_pretalk",
        "merchant_pretalk",
        "village_elder_pretalk",
        "ransom_broker_pretalk",
        "tavernkeeper_pretalk",
        "goods_merchant_pretalk",
        "tavern_traveler_pretalk",
        "gm_pretalk",
    ]:
        assert state in states

    for category in [
        "startup_and_dispatch",
        "lords_politics_family",
        "centers_economy",
        "townsfolk_special_npcs",
        "encounters_battles_prisoners",
        "companions_named_npcs",
        "misc_dialogs",
    ]:
        assert category in categories

    assert "Dialogue State Inventory" in rendered
    assert "High-Traffic Category States" in rendered


def test_dialogue_immersion_report_detects_shadowing_and_missing_coverage() -> None:
    module = load_report_module()
    shadowing, missing_coverage = module.detect_immersion_coverage_gaps()
    rendered = module.render()

    assert "## High-Traffic Immersion Shadowing" in rendered
    assert "## High-Traffic Immersion Coverage Gaps" in rendered
    assert isinstance(shadowing, list)
    assert isinstance(missing_coverage, list)
    for state, fallback_path, fallback_line, shadowed_path, shadowed_line in shadowing:
        assert state
        assert fallback_path
        assert isinstance(fallback_line, int)
        assert shadowed_path
        assert isinstance(shadowed_line, int)
    for state, gap_type, detail in missing_coverage:
        assert state
        assert gap_type
        assert detail


if __name__ == "__main__": 
    test_dialogue_immersion_report_covers_core_states_and_categories()
    test_dialogue_immersion_report_detects_shadowing_and_missing_coverage()
    print("test_dialogue_immersion_report_static: OK")
