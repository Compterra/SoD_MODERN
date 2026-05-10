from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_intro_pretender_comment_requires_supported_pretender() -> None:
    script = read("src/scripts/ZJ_notes_and_information/get_relevant_comment_for_log_entry.py")
    marker = '(assign, ":comment", "str_comment_intro_liege_affiliated")'
    assert marker in script
    before = script[: script.index(marker)]
    window = before[-220:]
    assert '(gt, "$supported_pretender", 0)' in window
    assert '(gt, "$players_kingdom", 0)' not in window


def test_unsupplied_pretender_start_states_are_guarded() -> None:
    start = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_56.py")
    member_chat = read("src/dialogs/ZA01_startup_and_dispatch/anyone_member_chat_03.py")
    assert '(eq, "$g_talk_troop", "$supported_pretender")' in start
    assert '(eq, "$g_talk_troop", "$supported_pretender")' in member_chat


def test_support_is_still_only_assigned_on_oath_conclusion() -> None:
    conclude = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_give_conclude.py")
    assert '(assign, "$supported_pretender", "$g_talk_troop")' in conclude
    intro = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_pretender_intro_3.py")
    story = read("src/dialogs/ZB01_lords_politics_and_family/anyone_pretender_rebellion_cause_1.py")
    assert "$supported_pretender" not in intro
    assert "$supported_pretender" not in story
