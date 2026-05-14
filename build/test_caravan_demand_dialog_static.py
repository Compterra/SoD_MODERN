from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def main() -> None:
    demand_entry = read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_talk_03.py")
    demand_decline = read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_demand_2_03.py")
    toll_decline = read("src/dialogs/ZC01_centers_and_economy/anyone_plyr_merchant_demand_toll_2_02.py")

    assert_contains(demand_entry, '(eq, "$talk_context", tc_party_encounter)')
    assert_contains(demand_entry, '(gt, "$g_encountered_party", 0)')
    assert_contains(demand_entry, '(party_is_active, "$g_encountered_party")')
    assert_contains(demand_entry, '(neq, "$g_encountered_party_faction", "$players_kingdom")')
    assert_contains(demand_entry, '(ge, "$g_talk_troop_faction_relation", 0)')
    assert_contains(demand_entry, "You will pay a toll for this road.")
    assert_not_contains(demand_entry, "I demand something from you!")

    assert_contains(demand_decline, "Keep your purse. Ride on.")
    assert_not_contains(demand_decline, "I will not press you")
    assert_not_contains(demand_decline, "the this road")

    assert_contains(toll_decline, "Keep the toll. Ride on.")
    assert_not_contains(toll_decline, "I will not dirty this road")

    print("test_caravan_demand_dialog_static: OK")


if __name__ == "__main__":
    main()
