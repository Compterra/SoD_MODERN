from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def main():
    change_script = read("src/scripts/ZD_centers/change_player_relation_with_center.py")
    assert '(is_between, ":center_no", centers_begin, centers_end)' in change_script, (
        "center relation changes must reject invalid party ids"
    )
    assert '(assign, ":center_no", "$sod_event_relation_center")' in change_script, (
        "center relation changes should fallback to the pinned event center when available"
    )

    pinned_event_files = [
        "src/menus/events/choice_04_1.py",
        "src/menus/events/choice_04b_1.py",
        "src/menus/events/choice_04d_1.py",
        "src/menus/events/choice_04f_1.py",
        "src/menus/events/choice_04h_1.py",
        "src/menus/events/choice_04h_1_02.py",
    ]
    for rel in pinned_event_files:
        source = read(rel)
        assert '(assign, "$sod_event_relation_center", reg0)' in source, (
            f"{rel} should pin its local event center before choices run"
        )
        assert '(neg|is_between, "$sod_event_relation_center", centers_begin, centers_end)' in source, (
            f"{rel} should guard against closest-center helpers returning -1"
        )
        assert 'script_change_player_relation_with_center", reg0' not in source, (
            f"{rel} should not apply center relations through volatile reg0"
        )
        assert 'script_change_player_relation_with_center", reg1' not in source, (
            f"{rel} should not apply center relations through volatile reg1"
        )

    event_04i = read("src/menus/events/choice_04h_1_02.py")
    assert '(party_get_num_companions, reg0, "p_main_party")' in event_04i, (
        "event_04i still computes its service cost in reg0"
    )
    assert 'script_change_player_relation_with_center", "$sod_event_relation_center", -2' in event_04i, (
        "event_04i must not use the service cost register as a center id"
    )

    print("Random event relation center static checks passed")


if __name__ == "__main__":
    main()

