from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devkit.troop_item_balance import troop_item_balance as balance


def main() -> None:
    index = balance.build_balance_index(ROOT)
    report = balance.balance_player_start_progression(index)

    assert report["state"] == "within_static_progression_targets", report["review_signals"]
    assert report["route_count"] == 52
    assert len(report["culture_summaries"]) == 5
    assert all(summary["route_count"] > 0 for summary in report["culture_summaries"])
    assert all(summary["review_route_count"] == 0 for summary in report["culture_summaries"])
    assert report["kit_trade_count"] == 5
    assert all(route["delta"]["level"] > 0 for route in report["routes"])
    assert all(route["rank_order_preserved"] for route in report["routes"])
    assert all(route["training_advantage_signals"] for route in report["routes"])
    assert all(not route["target_loadout_contract_issues"] for route in report["routes"])

    antarian_veteran = next(route for route in report["routes"] if route["target_id"] == "trp_sod_ant_veteran")
    assert antarian_veteran["progression_class"] == "training_compensated_kit_trade"
    assert {"combat_skills", "proficiencies"} <= set(antarian_veteran["training_advantage_signals"])
    print("test_player_start_progression_static: OK")


if __name__ == "__main__":
    main()
