from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_hourly_random_soldier_events_require_regular_troops() -> None:
    trigger = read("src/triggers/ST02_every_hour/entry_0110.py")
    assert '(call_script, "script_party_count_fit_regulars", "p_main_party")' in trigger
    assert "(gt, reg0, 0)" in trigger


def test_soldiers_go_home_event_selects_only_valid_regular_stacks() -> None:
    event = read("src/menus/events/choice_04g_1.py")
    assert '(assign, ":num_regular_stacks", 0)' in event
    assert '(neg|troop_is_hero, ":troop_id")' in event
    assert '(gt, ":size", 0)' in event
    assert '(gt, ":num_regular_stacks", 0)' in event
    assert '(store_add, ":random_upper", ":num_regular_stacks", 1)' in event
    assert '(assign, ":this_stack", -1)' in event
    assert '(ge, ":this_stack", 0)' in event


def test_related_desertion_events_use_same_regular_stack_guard() -> None:
    for path in (
        "src/menus/events/choice_22_1.py",
        "src/menus/events/choice_04a_1.py",
    ):
        event = read(path)
        assert '(assign, ":num_regular_stacks", 0)' in event
        assert '(gt, ":num_regular_stacks", 0)' in event
        assert '(store_add, ":random_upper", ":num_regular_stacks", 1)' in event
        assert '(neg|troop_is_hero, ":troop_id")' in event


if __name__ == "__main__":
    test_hourly_random_soldier_events_require_regular_troops()
    test_soldiers_go_home_event_selects_only_valid_regular_stacks()
    test_related_desertion_events_use_same_regular_stack_guard()
    print("test_random_soldiers_go_home_event_static: OK")

