from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    ROOT / "src" / "scripts" / "ZD_centers" / "cf_select_random_walled_center_with_faction_and_less_strength_pr.py",
    ROOT / "src" / "scripts" / "ZD_centers" / "cf_troop_get_random_leaded_walled_center_with_less_strength_prio.py",
]


def main() -> None:
    for path in SCRIPTS:
        source = path.read_text(encoding="utf-8")

        assert '(store_script_param, ":preferred_center_no", 2)' in source, path
        assert 'slot_center_is_besieged_by, -1' in source, path
        assert '(val_add, ":num_centers", 99)' in source or '(val_add, ":no_centers", 99)' in source, path
        assert '(val_sub, ":random_center", 99)' in source, path
        assert '(assign, reg0, ":result")' in source, path

        stale_needles = [
            "script_party_calculate_regular_strength",
            '":strength"',
            "(lt, \":strength\", 80)",
            "(val_div, \":strength\", 20)",
        ]
        for needle in stale_needles:
            assert needle not in source, f"{path}: {needle}"

    print("test_walled_center_priority_static: OK")


if __name__ == "__main__":
    main()
