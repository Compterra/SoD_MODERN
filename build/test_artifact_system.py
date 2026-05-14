# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def main() -> int:
    constants = read("src/constants/module_constants.py")
    registry = read("src/scripts/ZY_helper_scripts/sod_artifact_init_registry.py")
    delivery = read("src/scripts/ZY_helper_scripts/sod_royal_deliver_pending_artifact.py")
    progress = read("src/scripts/ZY_helper_scripts/sod_artifact_add_kill.py")
    milestone = read("src/scripts/ZY_helper_scripts/sod_artifact_unlock_milestone.py")
    maintainable = read("src/scripts/ZY_helper_scripts/sod_artifact_find_maintainable_weapon.py")
    equipped_set = read("src/scripts/ZY_helper_scripts/sod_artifact_check_equipped_set.py")
    doctrine_discount = read("src/scripts/ZY_helper_scripts/sod_artifact_get_doctrine_discount.py")
    doctrine_report = read("src/scripts/ZY_helper_scripts/sod_describe_elite_doctrine_report.py")
    smith = read("src/menus/reports/royal_artifact_smith.py")
    report = read("src/scripts/ZY_helper_scripts/sod_artifact_describe_reliquary_report.py")
    tooltip = read("src/scripts/ZY_helper_scripts/sod_artifact_describe_tooltip.py")
    extra_text = read("src/scripts/ZA_hardcoded_game_scripts/game_get_item_extra_text.py")
    capture = read("src/scripts/ZY_helper_scripts/sod_artifact_capture_spoils.py")
    mission_preamble = read("src/mission_templates/_preamble/00_imports.py")

    assert_contains(constants, "slot_item_artifact_flags")
    assert_contains(constants, "slot_item_artifact_technique_flags")
    assert_contains(constants, "artifact_tech_reinforced_haft")
    assert_contains(constants, "artifact_flag_weapon")
    assert_contains(constants, "artifact_progress_stride")

    assert_contains(registry, "sod_artifact_register_item")
    assert_contains(registry, "itm_blacksmith_adenian_armor")
    assert_contains(registry, "itm_items_end")
    assert_contains(registry, "artifact_flag_royal|artifact_flag_set_piece|artifact_flag_weapon")
    assert_contains(registry, "slot_item_artifact_original_owner")

    assert_contains(delivery, "sod_royal_deliver_pending_artifact")
    assert_contains(delivery, "slot_item_artifact_current_owner")
    assert_contains(delivery, "slot_item_artifact_last_modifier")

    assert_contains(progress, "sod_artifact_add_kill")
    assert_contains(progress, "script_sod_artifact_unlock_milestone")
    assert_contains(progress, "slot_item_artifact_current_owner")
    assert_contains(milestone, "artifact_tech_folded_steel")
    assert_contains(milestone, "display_message")

    assert_contains(maintainable, "sod_artifact_find_maintainable_weapon")
    assert_contains(maintainable, "ek_item_0")
    assert_contains(maintainable, "ek_item_3 + 1")
    assert_contains(maintainable, "artifact_flag_weapon")
    assert_contains(maintainable, "artifact_tech_reinforced_haft")
    assert_contains(maintainable, "eq, \":already_maintained\", 0")
    assert_contains(maintainable, "script_sod_artifact_get_progress")
    assert_contains(maintainable, "assign, reg4, \":kills\"")
    assert_contains(maintainable, "assign, reg5, \":next_mark\"")

    assert_contains(equipped_set, "sod_artifact_check_equipped_set")
    assert_contains(equipped_set, "ek_item_0")
    assert_contains(equipped_set, "ek_horse + 1")
    assert_contains(equipped_set, "artifact_flag_set_piece")
    assert_contains(equipped_set, "assign, reg1, \":family\"")

    assert_contains(doctrine_discount, "script_sod_artifact_check_equipped_set")
    assert_contains(doctrine_discount, "eq, \":equipped_family\", \":needed_family\"")
    assert_contains(doctrine_discount, "ge, \":equipped_pieces\", 5")
    assert_contains(doctrine_discount, "ge, \":equipped_pieces\", 3")
    assert_contains(doctrine_discount, "val_min, \":discount\", 20")
    assert_contains(doctrine_report, "wearing three or more matching royal set pieces")
    assert_contains(doctrine_report, "capped with the reliquary discount")

    assert_contains(smith, "script_sod_artifact_find_maintainable_weapon")
    assert_contains(smith, "script_sod_player_charge_gold")
    assert_contains(smith, "item_set_slot, \":item_no\", slot_item_artifact_current_owner, \"trp_player\"")
    assert_contains(smith, "Battle record: {reg21}/{reg22}")
    assert_contains(smith, "No equipped royal artifact weapon needs smith maintenance right now")
    if smith.find("script_sod_artifact_find_maintainable_weapon") > smith.find("script_sod_player_charge_gold"):
        raise AssertionError("Smith must find a maintainable artifact before charging gold")

    assert_contains(report, "script_sod_artifact_find_maintainable_weapon")
    assert_contains(report, "script_sod_artifact_check_equipped_set")
    assert_contains(report, "itm_items_end")
    assert_contains(report, "Smiths can maintain")
    assert_contains(report, "Equipped set")
    assert_contains(report, "restored royal image")
    assert_contains(report, "no equipped artifact weapon currently needs work")
    assert_contains(report, "assign, reg5, \":best_kills\"")
    assert_contains(tooltip, "Battle record")
    assert_contains(extra_text, "script_sod_artifact_describe_tooltip")

    assert_contains(capture, "sod_artifact_capture_spoils")
    assert_contains(capture, "script_sod_artifact_transfer_between_troops")
    assert_contains(mission_preamble, "script_sod_artifact_add_kill")

    print("[artifact_system] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

