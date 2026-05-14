from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_before(raw, first, second):
    first_index = raw.find(first)
    second_index = raw.find(second)
    assert first_index >= 0, f"missing expected token: {first}"
    assert second_index >= 0, f"missing expected token: {second}"
    assert first_index < second_index, f"expected {first!r} before {second!r}"


def main():
    trigger = read("src/triggers/ST01_every_frame/entry_0005.py")
    lodging_fee_trigger = read("src/triggers/ST02_every_hour/entry_0067.py")
    half_pay_trigger = read("src/triggers/ST02_every_hour/entry_0020.py")
    siege_wait_trigger = read("src/triggers/ST02_every_hour/entry_0003.py")

    assert_before(
        trigger,
        '(party_is_active, "$g_last_rest_center")',
        '(party_get_battle_opponent, ":besieger_party", "$g_last_rest_center")',
    )
    assert_before(
        trigger,
        '(party_is_active, ":besieger_party")',
        '(store_faction_of_party, ":besieger_party_faction", ":besieger_party")',
    )
    assert '(neg|party_is_active, "$g_last_rest_center")' in trigger
    assert '(assign, "$g_last_rest_center", -1)' in trigger

    assert_before(
        trigger,
        '(party_is_active, "$auto_enter_town")',
        '(start_encounter, "$auto_enter_town")',
    )
    assert_before(
        trigger,
        '(party_is_active, "$auto_besiege_town")',
        '(start_encounter, "$auto_besiege_town")',
    )
    assert '(assign, "$auto_enter_town", 0)' in trigger
    assert '(assign, "$auto_besiege_town", 0)' in trigger

    assert_before(
        lodging_fee_trigger,
        '(party_is_active, "$g_last_rest_center")',
        '(neg|party_slot_eq, "$g_last_rest_center", slot_town_lord, "trp_player")',
    )
    assert_before(
        lodging_fee_trigger,
        '(party_is_active, "$g_last_rest_center")',
        '(store_faction_of_party, ":center_faction", "$g_last_rest_center")',
    )
    assert_before(
        half_pay_trigger,
        '(party_is_active, "$g_last_rest_center")',
        '(this_or_next|party_slot_eq, "$g_last_rest_center", slot_center_has_manor, 1)',
    )
    assert_before(
        siege_wait_trigger,
        '(party_is_active, "$auto_besiege_town")',
        '(ge, "$g_siege_method", 1)',
    )
    assert_before(
        siege_wait_trigger,
        '(party_is_active, "$g_player_besiege_town")',
        '(ge, "$g_siege_method", 1)',
    )

    print("autoresume party globals static checks passed")


if __name__ == "__main__":
    main()
