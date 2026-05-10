from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def main():
    for rel in [
        "src/menus/other/continue_23.py",
        "src/menus/other/continue_24.py",
        "src/menus/other/continue_25.py",
        "src/menus/other/continue_27.py",
    ]:
        raw = read(rel)
        assert '("continue", [(neq, "$g_battle_result", 1)], "Continue..."' in raw, (
            f"{rel} should hide failure continue after a successful village-bandit battle"
        )

    infestation = read("src/menus/centers/village/village_bandits_defeated_accept_03.py")
    assert '(call_script, "script_change_player_relation_with_center", "$current_town", 5)' in infestation
    assert '(call_script, "script_change_player_relation_with_center", "$current_town", 3)' in infestation
    assert '(call_script, "script_change_player_relation_with_center", "$current_town", 4)' in infestation
    assert '(call_script, "script_change_player_relation_with_center", "$g_encountered_party"' not in infestation
    assert '(quest_slot_eq, "qst_eliminate_bandits_infesting_village", slot_quest_target_center, "$current_town")' in infestation
    assert '(quest_slot_eq, "qst_deal_with_bandits_at_lords_village", slot_quest_target_center, "$current_town")' in infestation

    for rel in [
        "src/menus/centers/village/village_bandits_defeated_accept.py",
        "src/menus/centers/village/village_bandits_defeated_accept_02.py",
        "src/menus/centers/village/village_bandits_defeated_accept_04.py",
    ]:
        raw = read(rel)
        assert '(call_script, "script_change_player_relation_with_center", "$g_encountered_party"' not in raw, (
            f"{rel} should use $current_town for village relation changes"
        )

    print("Village bandit result static checks passed")


if __name__ == "__main__":
    main()

