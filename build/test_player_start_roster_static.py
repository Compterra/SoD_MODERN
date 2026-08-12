from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devkit.troop_item_balance import troop_item_balance as balance


PLAYER_START_CONTRACT_CODES = {
    "SHIELD_GUARANTEED_BUT_NO_SHIELD_IN_INVENTORY",
    "MOUNTED_ROLE_WITHOUT_MOUNT_ITEM",
    "NO_WEAPON_ITEM",
}


def inventory_codes(index: balance.BalanceIndex, troop_code: str) -> list[str]:
    item_codes = {item.index: item.code for item in index.items}
    troop = index.troop_by_code[troop_code]
    return [item_codes[value] for value in troop.data[7] if isinstance(value, int)]


def main() -> None:
    index = balance.build_balance_index(ROOT)
    findings = balance.balance_outliers(index, domain="troops", limit=200)["findings"]
    player_start_contract_failures = [
        finding
        for finding in findings
        if finding["code"] in PLAYER_START_CONTRACT_CODES
        and finding["evidence"]["campaign_cohort"]["campaign_group"] == "player_start_cultures"
    ]
    assert not player_start_contract_failures, player_start_contract_failures

    assert "tab_shield_round_b" in inventory_codes(index, "sod_ade_archer")
    assert "tab_shield_kite_c" in inventory_codes(index, "sod_ade_veteran_archer")
    medium_cavalry_inventory = inventory_codes(index, "sod_ade_medium")
    assert medium_cavalry_inventory.count("lance") == 1
    assert "sword_medieval_b" in medium_cavalry_inventory

    progression = balance.balance_progression(index, roster="Adenian")
    medium_upgrade = next(
        edge
        for edge in progression["explicit_upgrade_edges"]
        if edge["source_id"] == "trp_sod_ade_light" and edge["target_id"] == "trp_sod_ade_medium"
    )
    assert medium_upgrade["delta"]["level"] > 0
    print("test_player_start_roster_static: OK")


if __name__ == "__main__":
    main()
