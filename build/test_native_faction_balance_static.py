from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devkit.troop_item_balance import troop_item_balance as balance


def require(text: str, token: str) -> None:
    assert token in text, f"Missing Native faction balance contract: {token}"


def main() -> None:
    templates = (ROOT / "compile/module_party_templates.py").read_text(encoding="utf-8", errors="replace")
    require(templates, '(trp_khergit_skirmisher,2,6),(trp_khergit_tribesman,3,6)')
    require(templates, '(trp_khergit_horse_archer,2,5),(trp_khergit_skirmisher,3,6)')

    report = balance.balance_native_kingdoms(balance.build_balance_index(ROOT))
    assert report["state"] == "within_static_balance_targets", report["review_signals"]
    assert report["kingdom_count"] == 5
    assert report["progression_route_count"] == 39
    assert all(contract["status"] == "present" for contract in report["source_contracts"])
    assert all(spread["within_target"] for spread in report["pressure_spreads"].values())
    assert all(spread["target_max_ratio"] == 1.45 for spread in report["pressure_spreads"].values())

    khergit = next(kingdom for kingdom in report["kingdoms"] if kingdom["kingdom"]["id"] == "kingdom_3")
    assert khergit["runtime_binding"]["template_codes"] == {
        "a": "kingdom_3_reinforcements_a",
        "b": "kingdom_3_reinforcements_b",
        "c": "kingdom_3_reinforcements_c",
    }
    assert khergit["templates"]["a"]["member_total"]["expected"] == 8.5
    assert khergit["templates"]["b"]["member_total"]["expected"] == 8
    assert khergit["progression"]["review_route_count"] == 0
    assert all(route["delta"]["level"] > 0 for kingdom in report["kingdoms"] for route in kingdom["progression"]["routes"])
    assert all(route["rank_order_preserved"] for kingdom in report["kingdoms"] for route in kingdom["progression"]["routes"])
    assert all(route["training_advantage_signals"] for kingdom in report["kingdoms"] for route in kingdom["progression"]["routes"])
    assert all(not route["target_loadout_contract_issues"] for kingdom in report["kingdoms"] for route in kingdom["progression"]["routes"])
    print("test_native_faction_balance_static: OK")


if __name__ == "__main__":
    main()
