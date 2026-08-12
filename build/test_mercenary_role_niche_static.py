from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devkit.troop_item_balance import troop_item_balance as balance


def require(text: str, token: str) -> None:
    assert token in text, f"Missing mercenary role-niche contract: {token}"


def main() -> None:
    role_fit = (ROOT / "src/scripts/ZY_helper_scripts/sod_merc_market_calculate_guild_role_fit.py").read_text(encoding="utf-8")
    roster = (ROOT / "src/scripts/ZY_helper_scripts/sod_merc_guild_get_contract_roster.py").read_text(encoding="utf-8")
    weight = (ROOT / "src/scripts/ZY_helper_scripts/sod_merc_market_calculate_kingdom_guild_weight.py").read_text(encoding="utf-8")
    demand = (ROOT / "src/scripts/ZY_helper_scripts/sod_merc_market_calculate_kingdom_demand.py").read_text(encoding="utf-8")
    accept = (ROOT / "src/scripts/ZY_helper_scripts/sod_merc_market_try_accept_bid.py").read_text(encoding="utf-8")
    spawn = (ROOT / "src/scripts/ZI_campaign_ai/cf_spawn_ai_mercs.py").read_text(encoding="utf-8")
    preview = (ROOT / "src/scripts/ZY_helper_scripts/merc_build_preview_party.py").read_text(encoding="utf-8")
    deployment = (ROOT / "src/scripts/ZY_helper_scripts/sod_merc_market_deploy_ai_contract.py").read_text(encoding="utf-8")
    dialogue = (ROOT / "src/scripts/ZY_helper_scripts/sod_merc_market_describe_ai_contract_to_s68.py").read_text(encoding="utf-8")

    for guild in range(1, 8):
        require(role_fit, f'"fac_sod_merc_guild{guild}"')
        require(roster, f'"fac_sod_merc_guild{guild}"')
        require(dialogue, f'"fac_sod_merc_guild{guild}"')
    for role in (
        "sod_merc_contract_role_patrol",
        "sod_merc_contract_role_escort",
        "sod_merc_contract_role_supply_column",
        "sod_merc_contract_role_garrison_support",
        "sod_merc_contract_role_special_world_activity",
    ):
        require(role_fit, role)
        require(roster, role)

    require(role_fit, '(assign, ":role_fit", -28)')
    require(role_fit, '(assign, ":role_fit", -18)')
    require(role_fit, '(assign, ":role_fit", -12)')
    require(weight, "script_sod_merc_market_calculate_guild_role_fit")
    require(weight, ":demand_type")
    require(demand, "script_sod_merc_market_select_preferred_guild")
    require(demand, ":need_type")
    require(spawn, "script_sod_merc_guild_get_contract_roster")
    require(spawn, ":specialist_units")
    require(spawn, '(val_sub, ":t1_2_units", ":specialist_units")')
    require(accept, "script_sod_merc_market_resolve_ai_contract_role")
    require(accept, ":effective_demand_type")
    assert "script_sod_merc_guild_get_contract_roster" not in preview, "Player hire preview must not infer an AI contract role."
    for mobile_role in (
        "sod_merc_contract_role_escort",
        "sod_merc_contract_role_mercenary_lord",
        "sod_merc_contract_role_special_world_activity",
    ):
        require(deployment, mobile_role)
    require(deployment, "Mobile jobs have no center target")
    require(deployment, "script_sod_merc_market_resolve_ai_contract_role")
    require(dialogue, "{s72}")
    require(dialogue, "slot_party_sod_merc_contract_guild")

    report = balance.balance_mercenary_guilds(balance.build_balance_index(ROOT))
    assert report["state"] == "within_static_niche_targets", report["source_contracts"]
    assert report["guild_count"] == 7
    assert report["missing_troop_ids"] == []
    assert all(contract["status"] == "present" for contract in report["source_contracts"])
    assert all(row["contract_niche"]["primary_roles"] for row in report["guilds"])
    assert next(row for row in report["guilds"] if row["guild"]["id"] == "slavers")["contract_niche"]["deprioritized_roles"]
    print("test_mercenary_role_niche_static: OK")


if __name__ == "__main__":
    main()
