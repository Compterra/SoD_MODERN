from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "scripts" / "ZD_centers" / "init_town_walkers.py"


def main() -> None:
    source = SCRIPT.read_text(encoding="utf-8")

    assert '("init_town_walkers",' in source
    assert '(eq, "$town_nighttime", 0)' in source
    assert '(try_for_range, ":walker_no", 0, num_town_walkers)' in source
    assert '(store_add, ":troop_slot", slot_center_walker_0_troop, ":walker_no")' in source
    assert '(party_get_slot, ":walker_troop_id", "$current_town", ":troop_slot")' in source
    assert '(store_add, ":entry_no", town_walker_entries_start, ":walker_no")' in source
    assert '(set_visitor, ":entry_no", ":walker_troop_id")' in source

    stale_needles = [
        '":cur_walker"',
        '":num_walkers"',
        '":walker_troop"',
        "(shuffle_range, 0, 8)",
        "(set_visitor, 32, reg0)",
    ]
    for needle in stale_needles:
        assert needle not in source, needle

    print("test_town_walkers_static: OK")


if __name__ == "__main__":
    main()
