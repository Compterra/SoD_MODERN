from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def main():
    constants = read("src/constants/module_constants.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_companion_post_battle_comment.py")
    companion_depth = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    victory = read("src/scripts/ZC_parties/total_victory_finalize.py")
    defeat = read("src/scripts/ZC_parties/event_player_captured_as_prisoner.py")
    duel = read("src/scripts/ZY_helper_scripts/ponavosa_duel_resolve.py")
    company = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    morale = read("src/scripts/ZZ_common_array_processing/morale_check.py")
    rout = read("src/scripts/ZZ_common_array_processing/rout_check.py")
    mission_preamble = read("src/mission_templates/_preamble/00_imports.py")

    for token in [
        "sod_companion_action_battle_defeat",
        "sod_companion_action_morale_collapse",
        "sod_companion_action_commander_duel_won",
        "sod_companion_action_commander_duel_lost",
        "sod_companion_action_mutiny_battle",
    ]:
        assert token in constants
        assert token in companion_depth

    assert "sod_companion_post_battle_comment" in helper
    assert "$g_sod_last_post_battle_comment_day" in helper
    assert "$g_sod_last_post_battle_comment_type" in helper
    assert "$g_sod_last_post_battle_comment_day" in company
    assert "$g_sod_last_post_battle_comment_type" in company
    assert '(assign, "$g_sod_battle_player_morale_wavered", 0)' in company
    assert '(assign, "$g_sod_battle_player_morale_collapsed", 0)' in company
    assert '(eq, "$g_sod_last_post_battle_comment_day", ":cur_day")' in helper
    assert '(eq, "$g_sod_last_post_battle_comment_type", ":comment_type")' in helper
    for phrase in [
        "A field can be won and still ask mercy of us.",
        "Defeat is a lesson only if command has the courage to read it.",
        "They saw more than one man fall there.",
        "Men do not run from one bad moment.",
        "This is what happens when a camp stops believing it can be heard.",
    ]:
        assert phrase in helper

    assert 'script_sod_companion_post_battle_comment", 1' in victory
    assert 'script_sod_companion_post_battle_comment", 3' in victory
    assert '(assign, "$g_sod_battle_player_morale_wavered", 0)' in victory
    assert '(assign, "$g_sod_battle_player_morale_collapsed", 0)' in victory
    assert 'script_sod_company_accounts_record_battle_defeat' in defeat
    assert 'script_sod_companion_post_battle_comment", -1' in defeat
    assert '(assign, "$g_sod_battle_player_morale_wavered", 0)' in defeat
    assert '(assign, "$g_sod_battle_player_morale_collapsed", 0)' in defeat
    assert 'script_sod_companion_post_battle_comment", 2' in duel
    assert 'script_sod_companion_post_battle_comment", -2' in duel
    assert 'script_sod_companion_post_battle_comment", 4' in company
    assert "$g_sod_battle_player_morale_wavered" in morale
    assert "$g_sod_battle_player_morale_collapsed" in rout
    assert "$g_sod_battle_player_morale_wavered" in mission_preamble
    assert "$g_sod_battle_player_morale_collapsed" in mission_preamble

    print("post battle comment static checks passed")


if __name__ == "__main__":
    main()
