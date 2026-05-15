from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def assert_order(raw: str, first: str, second: str) -> None:
    assert_contains(raw, first)
    assert_contains(raw, second)
    if raw.index(first) >= raw.index(second):
        raise AssertionError(f"{first} must precede {second}")


def main() -> int:
    center_identity = read("src/scripts/ZY_helper_scripts/sod_center_store_identity_line_to_s23.py")
    local_contact = read("src/scripts/ZY_helper_scripts/sod_show_local_contact_portrait.py")
    walled_center = read("src/menus/centers/castle/castle_castle.py")
    village = read("src/menus/centers/village/recruit_volunteers.py")
    siege_attack = read("src/menus/centers/castle/siege_request_meeting.py")
    siege_allies = read("src/menus/centers/castle/talk_to_siege_commander.py")
    siege_outside = read("src/menus/centers/castle/approach_besiegers.py")
    siege_defense = read("src/menus/centers/castle/siege_defender_join_battle.py")
    market = read("src/menus/centers/town/trade_with_arms_merchant.py")
    bank = read("src/menus/centers/town/sod_bank.py")
    guild_base = read("src/menus/centers/town/sod_merc_guild.py")
    guild_hall = read("src/menus/centers/castle/castle_mercenary_guild_hall.py")

    assert_contains(center_identity, '("sod_center_store_identity_line_to_s23"')
    assert_contains(center_identity, "Authority:")
    assert_contains(center_identity, "The watch is strained by road danger.")
    assert_contains(center_identity, "The local watch has the roads in hand.")
    assert_contains(center_identity, "script_sod_get_center_security_profile")
    assert_contains(walled_center, "{s23}")
    assert_contains(village, "{s23}")
    assert_contains(walled_center, 'script_sod_center_store_identity_line_to_s23')
    assert_contains(village, 'script_sod_center_store_identity_line_to_s23')

    assert_contains(siege_attack, 'script_sod_show_center_owner_portrait')
    assert_contains(siege_allies, 'script_sod_show_party_leader_portrait')
    assert_contains(siege_outside, 'script_sod_show_party_leader_portrait')
    assert_contains(siege_defense, 'script_sod_show_party_leader_portrait')
    assert_contains(siege_outside, '"{s72} has come under siege by {s73}."')
    assert_contains(siege_outside, '(str_store_string, s72, "@The center")')
    assert_contains(siege_outside, '(str_store_string, s73, "@the besiegers")')
    assert_order(
        siege_outside,
        '(party_is_active, "$g_encountered_party_2")',
        '(store_faction_of_party, ":faction_no", "$g_encountered_party_2")',
    )
    assert_order(
        siege_outside,
        '(party_is_active, "$g_encountered_party")',
        '(store_faction_of_party, ":faction_no", "$g_encountered_party")',
    )

    assert_contains(local_contact, '("sod_show_center_market_contact_portrait"')
    assert_contains(local_contact, '("sod_show_guild_contact_portrait"')
    assert_contains(market, 'script_sod_show_center_market_contact_portrait')
    assert_contains(bank, 'script_sod_show_center_market_contact_portrait')
    assert_contains(guild_base, 'script_sod_show_guild_contact_portrait')
    assert_contains(guild_hall, 'script_sod_show_guild_contact_portrait')

    print("[menu_identity_portraits_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
