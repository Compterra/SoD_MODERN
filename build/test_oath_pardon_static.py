from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(text, needle, label):
    if needle not in text:
        raise AssertionError(f"missing {label}: {needle}")


def assert_not_contains(text, needle, label):
    if needle in text:
        raise AssertionError(f"unexpected {label}: {needle}")


def main():
    terms = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_ask_pardon_after_oath_renounced_02.py")
    rejected = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_ask_pardon_terms_rejected.py")
    accepted = read("src/dialogs/ZB01_lords_politics_and_family/anyone_lord_ask_pardon_after_renounce_peace.py")

    assert_contains(terms, "$players_oath_renounced_begin_time", "pardon terms score uses oath-renounced timer")
    assert_contains(terms, "$players_oath_renounced_given_center", "pardon terms can remember demanded center")
    assert_contains(rejected, 'script_change_player_relation_with_troop", "$g_talk_troop", -5', "rejected terms lord relation penalty")
    assert_contains(rejected, '(store_current_hours, "$players_oath_renounced_begin_time")', "rejected terms resets pardon timer")
    assert_contains(rejected, '(assign, "$players_oath_renounced_given_center", 0)', "rejected terms clears demanded center")
    assert_contains(rejected, '(assign, "$players_oath_renounced_terms_state", 0)', "rejected terms clears state")
    assert_not_contains(rejected, "TODO", "stale pardon rejection TODO")
    assert_contains(accepted, "script_player_join_faction", "accepted pardon still rejoins faction")
    assert_contains(accepted, 'script_change_player_relation_with_troop", "$g_talk_troop", 3', "accepted pardon still improves lord relation")

    print("oath pardon static checks passed")


if __name__ == "__main__":
    main()
