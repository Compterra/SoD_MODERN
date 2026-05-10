from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def main():
    badboy = read("src/scripts/ZF_factions/change_badboy_rating.py")
    assert '(val_min, ":cur_badboy", 40)' in badboy, "badboy should be hard-capped at 40"
    assert '(assign, ":active_calradian_rivals", 0)' in badboy
    assert '(try_for_range, ":kingdom_no", "fac_kingdom_1", "fac_kingdom_6")' in badboy
    assert '(eq, ":active_calradian_rivals", 0)' in badboy
    assert '(assign, ":cur_badboy", 0)' in badboy, "badboy should clear when no Calradian rival realms remain"

    diplomacy = read("src/scripts/ZY_helper_scripts/sod_diplomacy_system.py")
    assert '(call_script, "script_change_badboy_rating", 3)' in diplomacy
    assert '(call_script, "script_change_badboy_rating", 4)' in diplomacy
    assert '(val_clamp, ":badboy", 0, 101)' not in diplomacy, (
        "diplomacy should use the centralized badboy script instead of direct 0..100 writes"
    )

    threat = read("src/scripts/ZD_centers/get_center_threat_level.py")
    assert '(is_between, ":center_no", centers_begin, centers_end)' in threat
    assert '(call_script, "script_sod_get_center_security_profile", ":center_no")' in threat
    assert '(display_log_message, "@Debug: get_center_threat_level ignored a non-center argument.", debug_color)' in threat

    relation = read("src/scripts/ZH_heroes/troop_get_player_relation.py")
    assert '(neq, ":faction", "fac_player_supporters_faction")' in relation
    assert '(eq, ":faction", "fac_player_supporters_faction")' not in relation, (
        "own lords should not grumble or cheer purely from player badboy"
    )

    upgrade = read("src/scripts/ZY_helper_scripts/sod_troop_can_upgrade_at_center.py")
    assert '(call_script, "script_sod_troop_can_faith_ascend_at_center", ":upgrade", ":center_no")' in upgrade
    assert '(call_script, "script_sod_troop_get_elite_tier", ":upgrade")' in upgrade
    assert '(neq, ":elite_tier", sod_elite_tier_faith)' in upgrade, (
        "valid faith ascensions should not be blocked by the generic faction-origin gate"
    )

    lord_dialog = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_chancellor_plyr_chancellor_lord_action_02.py")
    assert "There are no homeland lords left to recruit." in lord_dialog
    assert "Let's look at other topics to make decisions about." in lord_dialog

    print("Badboy, threat, lord recruitment, and zealot static checks passed")


if __name__ == "__main__":
    main()
