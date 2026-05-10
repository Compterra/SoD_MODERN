from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def main():
    fief = read("src/presentations/0020_sod_fief_management/sod_fief_management.py")
    artifacts = read("src/presentations/0021_sod_royal_artifacts/sod_royal_artifacts.py")

    for token in [
        '(val_max, ":value", 1)',
        '(val_clamp, ":value", 1, "$pres_sod_fief_buildings")',
        '(val_clamp, ":value", 0, ":daily_garrisoning")',
    ]:
        assert token in fief, f"missing fief presentation slider hardening: {token}"

    for token in [
        '(gt, ":mission_heroes", 0)',
        '(store_troop_gold, ":player_gold", "trp_player")',
        '(ge, ":player_gold", ":mission_gold")',
        '(party_count_members_of_type, ":available_heroes", "p_main_party", "$sod_royal_hero")',
        '(ge, ":available_heroes", ":mission_heroes")',
    ]:
        assert token in artifacts, f"missing royal artifact send validation: {token}"

    print("Presentation hardening static checks passed")


if __name__ == "__main__":
    main()
