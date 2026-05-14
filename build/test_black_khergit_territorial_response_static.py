# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def assert_not_contains(raw: str, needle: str) -> None:
    if needle in raw:
        raise AssertionError(f"Unexpected token: {needle}")


def main() -> int:
    constants = read("src/constants/module_constants.py")
    scripts = read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py")
    hourly = read("src/triggers/ST02_every_hour/entry_0159.py")
    simulate_battle = read("src/scripts/ZA_hardcoded_game_scripts/game_event_simulate_battle.py")

    for token in (
        "slot_party_black_khergit_response_until",
        "slot_party_black_khergit_response_target",
    ):
        assert_contains(constants, token)

    for token in (
        '"sod_black_khergits_process_ai_responses"',
        '"sod_black_khergits_note_ai_battle_outcome"',
        "pt_black_khergit_raiders",
        "pt_black_khergit_night_guard",
        "pt_black_khergit_horde_camp",
        "spt_kingdom_hero_party",
        "spt_patrol",
        "sod_support_type_castle_patrol",
        "sod_castle_patrol_status_active",
        "spai_engaging_army",
        "ai_bhvr_attack_party",
        "slot_party_sod_support_target",
        "slot_party_black_khergit_response_until",
        "slot_party_black_khergit_response_target",
        "Local riders are moving to challenge Black Khergit raiders",
        "A local warband has turned toward the Black Khergit camp",
        "Local defenders have broken a Black Khergit raider band",
        "Black Khergit riders have bloodied the local defense",
        "script_sod_black_khergits_scatter_or_cleanup_patrols",
        "slot_faction_black_khergit_camp_disrupted_until",
        "slot_faction_black_khergit_pressure",
    ):
        assert_contains(scripts, token)

    response_script = scripts.split('("sod_black_khergits_process_ai_responses"', 1)[1].split('("sod_black_khergits_note_ai_battle_outcome"', 1)[0]
    assert_contains(response_script, "(store_mod, \":hour_of_day\", \":cur_hours\", 24)")
    assert_contains(response_script, "(eq, \":is_day\", 1)")
    assert_contains(response_script, '(store_relation, ":player_relation", "fac_player_supporters_faction", "fac_black_khergits")')
    assert_contains(response_script, '(lt, ":player_relation", 100)')
    assert_contains(response_script, 'slot_party_black_khergit_response_target')
    assert_contains(response_script, '(neg|party_is_active, ":response_target")')
    assert_contains(response_script, "(le, \":defender_dist\", 24)")
    assert_contains(response_script, "(le, \":lord_dist\", 35)")
    assert_contains(response_script, "(ge, \":pressure\", 65)")
    assert_not_contains(response_script, "spt_player_mercenaries")
    assert_not_contains(response_script, "spt_player_patrol")

    outcome_script = scripts.split('("sod_black_khergits_note_ai_battle_outcome"', 1)[1].split('("sod_black_khergits_choose_bribed_target"', 1)[0]
    assert_contains(outcome_script, '(neq, ":winner_party", "p_main_party")')
    assert_contains(outcome_script, '(neq, ":defeated_party", "p_main_party")')
    assert_contains(outcome_script, '(assign, ":pressure_delta", -5)')
    assert_contains(outcome_script, '(assign, ":pressure_delta", -4)')
    assert_contains(outcome_script, '(assign, ":pressure_delta", -18)')
    assert_contains(outcome_script, '(assign, ":pressure_delta", 3)')
    assert_contains(outcome_script, '(neq, ":defeated_faction", "fac_black_khergits")')
    assert_contains(outcome_script, "spt_kingdom_hero_party")
    assert_contains(outcome_script, "spt_patrol")
    assert_contains(outcome_script, "spt_kingdom_caravan")
    assert_contains(outcome_script, "pt_merchant_caravan")

    refresh_script = scripts.split('("sod_black_khergits_refresh_active_parties"', 1)[1].split('("sod_black_khergits_apply_player_action"', 1)[0]
    assert_contains(refresh_script, '(eq, ":is_night", 1)')
    assert_contains(refresh_script, '(party_set_icon, ":party_no", "icon_camp")')
    assert_contains(refresh_script, '(party_set_ai_behavior, ":party_no", ai_bhvr_hold)')

    assert_contains(hourly, "script_sod_black_khergits_process_ai_responses")
    assert_contains(simulate_battle, "script_sod_black_khergits_note_ai_battle_outcome")

    print("[black_khergit_territorial_response_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
