from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "scripts" / "ZC_parties" / "cf_create_kingdom_party.py"


def assert_contains(source: str, needle: str) -> None:
    assert needle in source, f"missing expected kingdom party factory behavior: {needle}"


def assert_absent(source: str, needle: str) -> None:
    assert needle not in source, f"stale kingdom party factory block remains: {needle}"


def main() -> None:
    source = SCRIPT.read_text(encoding="utf-8")

    assert_contains(source, '("cf_create_kingdom_party",')
    assert_contains(source, '(faction_get_slot, ":reinforcements_b", ":faction_no", slot_faction_reinforcements_b)')
    assert_contains(source, '(eq, ":party_type", spt_kingdom_caravan)')
    assert_contains(source, '(assign, ":party_template", "pt_kingdom_caravan_party")')
    assert_contains(source, '(eq, ":party_type", spt_prisoner_train)')
    assert_contains(source, '(assign, ":party_template", "pt_prisoner_train_party")')
    assert_contains(source, '(call_script, "script_sod_find_prisoner_train_destination", ":spawn_center", ":faction_no", sod_prisoner_train_purpose_imprisonment)')
    assert_contains(source, '(call_script, "script_sod_load_prisoner_train_from_center_pool", ":result", ":spawn_center", 30, sod_prisoner_train_purpose_imprisonment)')
    assert_contains(source, '(call_script, "script_sod_add_prisoner_train_guards", ":result", ":faction_no", 1, sod_prisoner_train_purpose_imprisonment)')
    assert_contains(source, '(assign, reg0, ":result")')

    for stale in [
        '":reinforcements_a"',
        '":reinforcements_c"',
        "pt_forager_party",
        "pt_scout_party",
        "pt_patrol_party",
        "pt_messenger_party",
        "pt_raider_party",
        "pt_raider_captives",
        "slot_faction_messenger_troop",
    ]:
        assert_absent(source, stale)

    print("test_kingdom_party_factory_static: OK")


if __name__ == "__main__":
    main()
