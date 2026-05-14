from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def main():
    helper = read("src/scripts/ZY_helper_scripts/cf_sod_valid_lord_duel_target.py")
    for token in [
        '"cf_sod_valid_lord_duel_target"',
        "(is_between, \":troop_no\", kingdom_heroes_begin, kingdom_heroes_end)",
        "(troop_slot_eq, \":troop_no\", slot_troop_occupation, slto_kingdom_hero)",
        "(neg|troop_slot_eq, \":troop_no\", slot_troop_occupation, slto_dead)",
        "(neg|troop_slot_ge, \":troop_no\", slot_troop_prisoner_of_party, 0)",
        "(neg|is_between, \":troop_no\", pretenders_begin, pretenders_end)",
    ]:
        assert token in helper, f"missing duel target validation token: {token}"

    convince_menu = read("src/menus/duels/convince_duel.py")
    assert "script_cf_sod_valid_lord_duel_target" in convince_menu
    assert '(assign, ":duel_target", "$g_talk_troop")' in convince_menu
    assert '(set_visitor, 1, ":duel_target")' in convince_menu
    assert '(set_visitor, 1, "$g_talk_troop")' not in convince_menu

    convince_dialog = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_convince_duel_02.py")
    assert 'script_cf_sod_valid_lord_duel_target", "$g_talk_troop"' in convince_dialog

    lady_dialog = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_challenge_duel_for_lady_3.py")
    assert "script_cf_sod_valid_lord_duel_target" in lady_dialog
    assert '(set_visitor, 1, ":duel_target")' in lady_dialog
    assert '(set_visitor, 1, "$g_talk_troop")' not in lady_dialog

    random_quest = read("src/scripts/ZG_quests/get_random_quest.py")
    assert random_quest.count("script_cf_sod_valid_lord_duel_target") >= 4
    assert "Remove this when test is done" not in random_quest
    assert '(assign, ":quest_no", "qst_meet_spy_in_enemy_town")' not in random_quest

    for rel in [
        "src/mission_templates/0039_arena_challenge_fight/arena_challenge_fight.py",
        "src/mission_templates/0043_sod_arena_duel_fight/sod_arena_duel_fight.py",
    ]:
        raw = read(rel)
        assert "mtf_commit_casualties" not in raw, f"{rel} should not commit casualties in formal lord duels"

    print("Lord duel safety static checks passed")


if __name__ == "__main__":
    main()

