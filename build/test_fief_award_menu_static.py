from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(source: str, needle: str, label: str) -> None:
    assert needle in source, f"{label}: missing {needle}"


def assert_order(source: str, first: str, second: str, label: str) -> None:
    assert first in source, f"{label}: missing {first}"
    assert second in source, f"{label}: missing {second}"
    assert source.index(first) < source.index(second), f"{label}: {first} must precede {second}"


def test_unsolicited_fief_offer_guards_stale_center_global() -> None:
    menu = read("src/menus/centers/common/give_center_to_player_accept.py")

    for token in (
        '(str_store_string, s2, "@the disputed fief")',
        '(is_between, "$g_center_to_give_to_player", centers_begin, centers_end)',
        '("give_center_to_player_accept", [(is_between, "$g_center_to_give_to_player", centers_begin, centers_end)]',
        '("give_center_to_player_reject", [(is_between, "$g_center_to_give_to_player", centers_begin, centers_end)]',
        '("give_center_to_player_invalid_return", [(neg|is_between, "$g_center_to_give_to_player", centers_begin, centers_end)]',
        '(assign, "$g_center_to_give_to_player", -1)',
    ):
        assert_contains(menu, token, "fief offer")

    assert_order(
        menu,
        '(is_between, "$g_center_to_give_to_player", centers_begin, centers_end)',
        '(store_faction_of_party, ":center_faction", "$g_center_to_give_to_player")',
        "fief offer",
    )


def test_requested_fief_award_only_applies_to_valid_center() -> None:
    menu = read("src/menus/other/continue_18.py")

    for token in (
        '(str_store_string, s68, "@A messenger arrives with confused orders.',
        '(assign, ":award_center_valid", 0)',
        '(is_between, "$g_center_to_give_to_player", centers_begin, centers_end)',
        '(assign, ":award_center_valid", 1)',
        '(eq, ":award_center_valid", 1)',
        '(call_script, "script_give_center_to_lord", "$g_center_to_give_to_player", "trp_player", 0)',
        '(assign, "$g_center_to_give_to_player", -1)',
    ):
        assert_contains(menu, token, "requested fief award")

    assert_order(
        menu,
        '(is_between, "$g_center_to_give_to_player", centers_begin, centers_end)',
        '(call_script, "script_give_center_to_lord", "$g_center_to_give_to_player", "trp_player", 0)',
        "requested fief award",
    )


def test_fief_award_confirmation_has_invalid_fallback() -> None:
    menu = read("src/menus/other/continue_19.py")

    for token in (
        '(str_store_string, s2, "@the awarded fief")',
        '(str_store_string, s68, "@The confirmation cannot be completed because the awarded fief can no longer be resolved.")',
        '(is_between, "$g_center_to_give_to_player", centers_begin, centers_end)',
        '(str_store_string, s69, "@ and its bound village {s4}")',
        '(str_store_string, s68, "@With a brief ceremony, you are officially confirmed as the new lord of {s2}{s69}.',
    ):
        assert_contains(menu, token, "fief confirmation")


def test_denied_fief_decision_guards_center_and_owner_text() -> None:
    menu = read("src/menus/other/accept_decision.py")

    for token in (
        '"{s68}"',
        '(str_store_string, s5, "@another lord")',
        '(str_store_string, s69, "@fief")',
        '(assign, reg6, 0)',
        '(is_between, "$g_center_to_give_to_player", centers_begin, centers_end)',
        '(party_slot_eq, "$g_center_to_give_to_player", slot_party_type, spt_town)',
        '(party_slot_eq, "$g_center_to_give_to_player", slot_party_type, spt_castle)',
        '(is_between, ":new_owner", kingdom_heroes_begin, kingdom_heroes_end)',
        '("leave_faction", [(is_between, "$g_center_to_give_to_player", centers_begin, centers_end)]',
        'Renounce your oath',
    ):
        assert_contains(menu, token, "denied fief decision")

    assert_order(
        menu,
        '(assign, reg6, 0)',
        '(assign, reg6, 900)',
        "denied fief decision",
    )


def test_renounce_oath_hold_fief_path_guards_stale_center_global() -> None:
    menu = read("src/menus/kingdom/leave_faction_give_back.py")

    for token in (
        '(str_store_string, s2, "@the disputed fief")',
        '(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end)',
        '(is_between, "$g_center_to_give_to_player", centers_begin, centers_end)',
        '(call_script, "script_give_center_to_lord", "$g_center_to_give_to_player", "trp_player", 0)',
        '(party_set_slot, "$g_center_to_give_to_player", slot_center_faction_when_oath_renounced, "$players_oath_renounced_against_kingdom")',
        '(assign, "$g_center_to_give_to_player", -1)',
    ):
        assert_contains(menu, token, "renounce oath")

    assert_order(
        menu,
        '(is_between, "$g_center_to_give_to_player", centers_begin, centers_end)',
        '(str_store_party_name, s2, "$g_center_to_give_to_player")',
        "renounce oath",
    )


def test_hourly_fief_award_trigger_sets_center_global_from_valid_center_range() -> None:
    trigger = read("src/triggers/ST02_every_hour/entry_0066.py")

    for token in (
        '(try_for_range, ":center_no", centers_begin, centers_end)',
        '(party_slot_eq, ":center_no", slot_town_lord, stl_reserved_for_player)',
        '(assign, "$g_center_to_give_to_player", ":center_no")',
        '(jump_to_menu, "mnu_requested_castle_granted_to_player")',
        '(jump_to_menu, "mnu_give_center_to_player")',
        '(jump_to_menu, "mnu_requested_castle_granted_to_another")',
    ):
        assert_contains(trigger, token, "fief award trigger")

    assert_order(
        trigger,
        '(try_for_range, ":center_no", centers_begin, centers_end)',
        '(assign, "$g_center_to_give_to_player", ":center_no")',
        "fief award trigger",
    )


def test_player_faction_unassigned_center_trigger_repairs_player_owned_centers() -> None:
    trigger = read("src/triggers/ST02_every_hour/entry_0045.py")

    for token in (
        '(assign, "$g_center_taken_by_player_faction", -1)',
        '(store_faction_of_party, ":center_faction", ":center_no")',
        '(eq, ":center_faction", "fac_player_supporters_faction")',
        '(str_store_party_name_link, s2, "$g_center_taken_by_player_faction")',
        '(party_get_slot, reg1, "$g_center_taken_by_player_faction", slot_town_lord)',
        '(call_script, "script_give_center_to_lord", "$g_center_taken_by_player_faction", "trp_player", 0)',
        '@{s2} has been confirmed under your personal authority.',
        '(is_between, ":leader", kingdom_heroes_begin, kingdom_heroes_end)',
        '(start_map_conversation, ":leader")',
    ):
        assert_contains(trigger, token, "player faction unassigned center trigger")

    assert ':center_no", slot_town_lord)' not in trigger, (
        "player faction trigger must not read :center_no after the loop; "
        "use $g_center_taken_by_player_faction"
    )
    assert_order(
        trigger,
        '(party_get_slot, reg1, "$g_center_taken_by_player_faction", slot_town_lord)',
        '(call_script, "script_give_center_to_lord", "$g_center_taken_by_player_faction", "trp_player", 0)',
        "player faction unassigned center trigger",
    )


def test_center_captured_advice_dialog_guards_center_and_avoids_visible_s0() -> None:
    entry = read("src/dialogs/ZA01_startup_and_dispatch/anyone_event_triggered_03.py")
    player_request = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_center_captured_lord_advice.py")
    ruler_request = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_center_captured_lord_advice_02.py")
    troop_request = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_repeat_for_troops_center_captured_lord_advice.py")
    assignment = read("src/dialogs/ZB01_lords_politics_and_family/anyone_center_captured_lord_advice_2.py")

    assert_contains(
        entry,
        '(is_between, "$g_center_taken_by_player_faction", centers_begin, centers_end)',
        "center captured advice entry",
    )

    for label, source in (
        ("player request", player_request),
        ("ruler request", ruler_request),
        ("troop request", troop_request),
    ):
        assert_contains(source, '(str_store_string_reg, s69, s0)', label)
        assert "{s0}" not in source, f"{label}: visible fief list should use s69, not s0"
        assert "{s69}" in source, f"{label}: visible fief list should use s69"

    for token in (
        '(is_between, "$g_center_taken_by_player_faction", centers_begin, centers_end)',
        '(this_or_next|eq, "$temp", "trp_player")',
        '(is_between, "$temp", kingdom_heroes_begin, kingdom_heroes_end)',
        '(this_or_next|eq, ":new_owner", "trp_player")',
        '(is_between, ":new_owner", kingdom_heroes_begin, kingdom_heroes_end)',
        '(call_script, "script_give_center_to_lord", "$g_center_taken_by_player_faction", ":new_owner", 0)',
        '(assign, "$g_center_taken_by_player_faction", -1)',
    ):
        assert_contains(assignment, token, "center captured advice assignment")

    assert_order(
        assignment,
        '(is_between, "$g_center_taken_by_player_faction", centers_begin, centers_end)',
        '(call_script, "script_give_center_to_lord", "$g_center_taken_by_player_faction", ":new_owner", 0)',
        "center captured advice assignment",
    )
