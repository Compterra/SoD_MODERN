from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def script_block(raw: str, script_name: str) -> str:
    start = raw.index(f'("{script_name}"')
    next_start = raw.find('\n("', start + 1)
    return raw[start:] if next_start < 0 else raw[start:next_start]


def main() -> None:
    constants = read("src/constants/module_constants.py")
    maintenance = read("src/scripts/ZI_campaign_ai/sod_hourly_lord_ai_maintenance.py")

    for token in (
        "slot_center_sod_siege_attacker_strength_cache",
        "slot_center_sod_siege_marshall_attacking_cache",
    ):
        assert_contains(constants, token)

    reset = script_block(maintenance, "sod_siege_reset_attacker_strength_caches")
    accumulate = script_block(maintenance, "sod_siege_accumulate_attacker_strength_for_center")
    refresh = script_block(maintenance, "sod_siege_refresh_attacker_strength_caches")
    process = script_block(maintenance, "sod_process_siege_assault_decisions")

    assert_contains(reset, "walled_centers_begin, walled_centers_end")
    assert_contains(reset, "slot_center_sod_siege_attacker_strength_cache, 0")
    assert_contains(reset, "slot_center_sod_siege_marshall_attacking_cache, 0")

    for token in (
        "slot_center_is_besieged_by",
        "slot_center_sod_siege_attacker_strength_cache",
        "slot_center_sod_siege_marshall_attacking_cache",
        "script_party_calculate_regular_strength",
        "slot_lord_self_confidence",
    ):
        assert_contains(accumulate, token)

    assert_contains(refresh, "script_sod_siege_reset_attacker_strength_caches")
    assert_contains(refresh, 'try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end')
    assert_contains(refresh, "slot_party_commander_party")
    assert_contains(refresh, "script_sod_siege_accumulate_attacker_strength_for_center")

    assert_contains(process, "script_sod_siege_refresh_attacker_strength_caches")
    assert_contains(process, "slot_center_sod_siege_attacker_strength_cache")
    assert_contains(process, "slot_center_sod_siege_marshall_attacking_cache")
    assert process.index("script_sod_siege_refresh_attacker_strength_caches") < process.index(
        'try_for_range, ":center_no", walled_centers_begin, walled_centers_end'
    )
    assert_not_contains(process, 'script_party_calculate_regular_strength", ":party_no"')
    assert_contains(process, "script_party_calculate_regular_strength\", \"p_collective_enemy\"")

    print("test_siege_assault_refactor_static: OK")


if __name__ == "__main__":
    main()
