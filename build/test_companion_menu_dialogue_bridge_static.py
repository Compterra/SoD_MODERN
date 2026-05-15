# -*- coding: utf-8 -*-
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

COMPANION_MENU_BRIDGES = {
    "src/menus/camp/borcha_road_keeps_own.py": ("mnu_borcha_road_keeps_own", "trp_npc1"),
    "src/menus/camp/marnid_honest_price.py": ("mnu_marnid_honest_price", "trp_npc2"),
    "src/menus/camp/ymira_mercy_under_arms.py": ("mnu_ymira_mercy_under_arms", "trp_npc3"),
    "src/menus/camp/rolf_name_worth_wearing.py": ("mnu_rolf_name_worth_wearing", "trp_npc4"),
    "src/menus/camp/baheshtur_unbroken_saddle.py": ("mnu_baheshtur_unbroken_saddle", "trp_npc5"),
    "src/menus/camp/firentis_debt_restitution.py": ("mnu_firentis_debt_restitution", "trp_npc6"),
    "src/menus/camp/deshavi_tracks_through_ash.py": ("mnu_deshavi_tracks_through_ash", "trp_npc7"),
    "src/menus/camp/matheld_no_backward_step.py": ("mnu_matheld_no_backward_step", "trp_npc8"),
    "src/menus/camp/alayen_standard_self.py": ("mnu_alayen_standard_self", "trp_npc9"),
    "src/menus/camp/bunduk_men_hold_line.py": ("mnu_bunduk_men_hold_line", "trp_npc10"),
    "src/menus/camp/katrin_last_coin.py": ("mnu_katrin_last_coin", "trp_npc11"),
    "src/menus/camp/jeremus_hands_triage.py": ("mnu_jeremus_hands_triage", "trp_npc12"),
    "src/menus/camp/nizar_impossible_charge.py": ("mnu_nizar_impossible_charge", "trp_npc13"),
    "src/menus/camp/lezalit_discipline_without_chains.py": ("mnu_lezalit_discipline_without_chains", "trp_npc14"),
    "src/menus/camp/artimenner_siege_that_should.py": ("mnu_artimenner_siege_that_should", "trp_npc15"),
    "src/menus/camp/klethi_knife_with_name.py": ("mnu_klethi_knife_with_name", "trp_npc16"),
}


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def test_companion_world_event_menus_return_to_dialogue_for_resolution() -> None:
    for rel, (menu_id, troop_id) in COMPANION_MENU_BRIDGES.items():
        raw = read(rel)
        stale_self_jump = f'(jump_to_menu, "{menu_id}")'
        assert stale_self_jump not in raw, f"{rel}: should not loop back into its own choice menu"
        bridge = f'(start_map_conversation, "{troop_id}")'
        assert bridge in raw, f"{rel}: world-event aftermath should return to companion dialogue"


def test_companion_campfire_stays_as_an_entry_point_not_a_choice_wall() -> None:
    campfire = read("src/menus/camp/companion_campfire.py")
    assert "{s68}" in campfire
    assert "script_sod_companion_describe_campfire_to_s68" in campfire
    assert "{s1}" not in campfire
    assert "script_sod_companion_describe_campfire_to_s1" not in campfire
    assert campfire.count('("companion_campfire_back"') == 1
    for stale in (
        "script_sod_companion_assign_role",
        "script_sod_companion_advance_personal_quest",
        "companion_campfire_acknowledge_warnings",
        "companion_campfire_repair_acknowledged_warnings",
        "mnu_companion_depth_report",
        "mnu_companion_company_report",
    ):
        assert stale not in campfire, f"campfire menu is drifting back into dialogue/report work: {stale}"


if __name__ == "__main__":
    test_companion_world_event_menus_return_to_dialogue_for_resolution()
    test_companion_campfire_stays_as_an_entry_point_not_a_choice_wall()
    print("test_companion_menu_dialogue_bridge_static: OK")
