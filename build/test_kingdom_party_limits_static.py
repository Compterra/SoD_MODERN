from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "scripts" / "ZC_parties" / "create_kingdom_party_if_below_limit.py"


def main() -> None:
    source = SCRIPT.read_text(encoding="utf-8")

    assert '("create_kingdom_party_if_below_limit",' in source
    assert '(call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", ":party_type")' in source
    assert '(assign, ":party_count_limit", 0)' in source
    assert '(eq, ":party_type", spt_kingdom_caravan)' in source
    assert '(assign, ":party_count_limit", 5)' in source
    assert '(eq, ":party_type", spt_prisoner_train)' in source
    assert '(assign, ":party_count_limit", peak_prisoner_trains)' in source
    assert '(call_script, "script_cf_create_kingdom_party", ":faction_no", ":party_type")' in source

    stale_needles = [
        "spt_forager",
        "spt_scout",
        "spt_patrol",
        "spt_messenger",
    ]
    for needle in stale_needles:
        assert needle not in source, needle

    print("test_kingdom_party_limits_static: OK")


if __name__ == "__main__":
    main()
