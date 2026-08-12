from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devkit.troop_item_balance import troop_item_balance as balance


def inventory_codes(index: balance.BalanceIndex, troop_code: str) -> list[str]:
    item_codes = {item.index: item.code for item in index.items}
    troop = index.troop_by_code[troop_code]
    return [item_codes[value] for value in troop.data[7] if isinstance(value, int)]


def main() -> None:
    index = balance.build_balance_index(ROOT)
    report = balance.balance_faith_ascensions(index)

    assert report["state"] == "within_static_tier_targets", report["review_signals"]
    assert report["route_count"] == 25
    assert report["expected_route_count"] == 25
    assert not report["missing_route_pairs"]
    assert all(route["source_rank"] == "Noble" for route in report["routes"])
    assert all(route["target_rank"] == "Faith/Zealot" for route in report["routes"])
    assert all(route["faith_advantage_signals"] for route in report["routes"])
    assert all(not route["target_loadout_contract_issues"] for route in report["routes"])

    wanderer = next(route for route in report["routes"] if route["faith_target_id"] == "trp_sod_faith4_mount_ranged")
    assert "steel_shield" in inventory_codes(index, "sod_faith4_mount_ranged")
    assert wanderer["kit_score_delta"] > 0
    print("test_faith_tier_balance_static: OK")


if __name__ == "__main__":
    main()
