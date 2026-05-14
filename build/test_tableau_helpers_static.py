from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def main() -> int:
    helper = read("src/scripts/ZY_helper_scripts/sod_get_tableau_troop_seed.py")
    for token in (
        '"sod_get_tableau_troop_seed"',
        '(troop_is_hero, ":troop_no")',
        '(assign, ":seed", -1)',
        '(store_mul, ":seed", ":troop_no", 126233)',
        '(val_mod, ":seed", 1000)',
        '(val_add, ":seed", 1)',
        '(assign, reg0, ":seed")',
    ):
        assert token in helper, f"missing tableau seed helper token: {token}"

    for rel in (
        "src/scripts/ZH_heroes/add_troop_to_cur_tableau_for_inventory.py",
        "src/scripts/ZH_heroes/add_troop_to_cur_tableau_for_character.py",
        "src/scripts/ZC_parties/add_troop_to_cur_tableau_for_party.py",
    ):
        raw = read(rel)
        assert 'script_sod_get_tableau_troop_seed' in raw, rel
        assert '(cur_tableau_add_troop, ":troop_no", pos2, ":animation", reg0)' in raw, rel
        assert '":random_seed"' not in raw, rel

    print("test_tableau_helpers_static: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
