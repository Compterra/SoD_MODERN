from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_khergit_chieftain_has_quest_captive_prisoner_dialogue() -> None:
    order = read("src/dialogs/_order_dialogs.txt")
    generic = "ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_04.py"
    quest = "ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_quest_captive.py"
    assert quest in order
    assert order.index(quest) < order.index(generic)

    dialogue = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_quest_captive.py")
    assert '(eq, "$g_talk_troop", "trp_khergit_chieftain")' in dialogue
    assert '(check_quest_active, "qst_elephant_guard_capture_the_bastard")' in dialogue
    assert "There will be no bargain" in dialogue


def test_generic_prisoner_recruitment_excludes_heroes() -> None:
    commoner = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_04.py")
    already_agreed_room = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_02.py")
    already_agreed_no_room = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_03.py")
    offer = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_prisoner_chat_offer.py")

    for source in (commoner, already_agreed_room, already_agreed_no_room, offer):
        assert '(neg|troop_is_hero, "$g_talk_troop")' in source

    assert '(neq, "$g_talk_troop", "trp_khergit_chieftain")' in offer


def test_agreement_script_refuses_heroes_and_chieftain() -> None:
    script = read("src/scripts/ZC_parties/determine_prisoner_agreed.py")
    assert '(this_or_next|troop_is_hero, ":prisoner")' in script
    assert '(eq, ":prisoner", "trp_khergit_chieftain")' in script
    assert '(troop_set_slot, ":prisoner", slot_prisoner_agreed, 0)' in script
