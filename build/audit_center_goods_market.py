from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "reports" / "center_goods_market_audit.md"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    profile = read("src/scripts/ZY_helper_scripts/sod_center_goods_market_profile.py")
    trigger = read("src/triggers/ST04_weekly/entry_0160.py")
    price_update = read("src/scripts/ZB_economy_and_trade/update_trade_good_price_for_party.py")
    village_production = read("src/triggers/ST99_other/entry_0036.py")
    town_consumption = read("src/triggers/ST04_weekly/entry_0019.py")
    wealth_clamp = 'val_clamp, ":wealth_delta", -500, 1801'

    outputs = [
        ("reg0", "food balance", "Food production minus market/castle consumption pressure."),
        ("reg1", "raw balance", "Wool, pottery, linen, and furs available for workshop and rural export flow."),
        ("reg2", "strategic balance", "Salt, iron, oil, and tools available for logistics and productive support."),
        ("reg3", "luxury flow", "Spice and velvet flow that creates high-value but lower-volume liquidity."),
        ("reg4", "scarcity pressure", "Trade demand scarcity plus food and strategic shortages."),
        ("reg5", "trade willingness", "Security-adjusted willingness for merchants to answer demand."),
        ("reg6", "liquidity pressure", "Bounded weekly market pressure from surplus, scarcity, security, and taxes."),
        ("reg7", "wealth delta", "Bounded weekly wealth drift applied to the center."),
        ("reg8", "prosperity pressure", "Small prosperity nudge from strong liquidity or severe scarcity."),
        ("reg9", "market role", "1 village producer, 2 castle military consumer, 3 town market engine."),
    ]

    goods = [
        ("Food", "`grain`, `flour`, `bread`, `cabbages`, `apples`, meats, dairy, ale, wine", "Towns consume heavily; shortages raise scarcity and can slow recovery."),
        ("Raw", "`wool`, `pottery`, `linen`, `furs`", "Villages and rural hinterlands feed workshop and export liquidity."),
        ("Strategic", "`salt`, `iron`, `oil`, `tools`", "Castles and production systems care about these as logistics inputs."),
        ("Luxury", "`spice`, `velvet`", "High-value flow increases liquidity without acting like food security."),
    ]

    lines = [
        "# Center Goods Market Audit",
        "",
        "This report documents the shared goods-market profile that connects trade-good production, scarcity, caravan willingness, center wealth/liquidity, and prosperity pressure.",
        "",
        "## Summary",
        "",
        "- Weekly goods-market drift is implemented in `src/triggers/ST04_weekly/entry_0160.py`.",
        "- The profile reads `script_sod_get_center_trade_demand_profile`, real trade-good production slots, security willingness, tax friction, and effective trade volume.",
        "- The resulting wealth delta is clamped so goods markets can push recovery or decline without replacing caravans, taxes, raids, and investments.",
        "",
        "## Goods Groups",
        "",
        "| Group | Items | Gameplay role |",
        "| --- | --- | --- |",
    ]
    for group, items, role in goods:
        lines.append(f"| {group} | {items} | {role} |")

    lines += [
        "",
        "## Profile Outputs",
        "",
        "| Register | Meaning | Notes |",
        "| --- | --- | --- |",
    ]
    for reg, meaning, notes in outputs:
        lines.append(f"| `{reg}` | {meaning} | {notes} |")

    lines += [
        "",
        "## Center Roles",
        "",
        "| Center type | Market behavior |",
        "| --- | --- |",
        "| Village | Producer/export root. Surplus goods create modest liquidity; fragility and poor security reduce reliability through the trade-demand and village-output profiles. |",
        "| Castle | Military consumer. Food and strategic shortages matter more than ordinary market services; wealth drift is intentionally smaller than towns. |",
        "| Town | Market engine. Rural surplus, services, caravan attractiveness, and security convert goods flow into wealth/liquidity. |",
        "",
        "## Static Checks",
        "",
        f"- Profile helper present: {'yes' if 'sod_get_center_goods_market_profile' in profile else 'no'}",
        f"- Weekly wealth hook present: {'yes' if 'script_sod_change_center_wealth' in trigger else 'no'}",
        f"- Prosperity pressure hook present: {'yes' if 'script_change_center_prosperity' in trigger else 'no'}",
        f"- Local scarcity hook present: {'yes' if 'script_sod_change_center_local_prosperity' in trigger else 'no'}",
        f"- Wealth delta clamp present: {'yes' if wealth_clamp in profile else 'no'}",
        f"- Price pressure hook present: {'yes' if 'profile_price_shift' in price_update and 'script_sod_get_center_goods_market_profile' in price_update else 'no'}",
        f"- Village production feedback present: {'yes' if 'production_feedback_pct' in village_production and 'script_sod_get_center_goods_market_profile' in village_production else 'no'}",
        f"- Town finished-goods feedback present: {'yes' if 'finished_output' in town_consumption and 'itm_tools' in town_consumption else 'no'}",
        f"- Castle military-store consumption present: {'yes' if 'castle_store_consumption' in town_consumption and 'castles_begin' in town_consumption else 'no'}",
        "",
        "## Price Pressure",
        "",
        "Trade-good prices now combine merchant shelf stock with the shared market profile. Food shortages, raw-material shortages, strategic shortages, broad scarcity, and unsafe trade willingness all move prices inside a bounded `profile_price_shift` clamp.",
        "",
        "## Production Feedback",
        "",
        "- Villages use the goods-market profile to moderate food and raw-material output; fragile, unsafe, or severe-scarcity markets produce less reliably.",
        "- Towns consume food while converting safe rural surplus and liquidity into finished goods such as tools, linen, pottery, and limited velvet.",
        "- Castles draw down food and strategic stores as military consumers, keeping their economy distinct from town markets.",
        "",
    ]

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
