# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "reports" / "food_reference_audit.md"


HOOKS = (
    ("Food profile", "src/scripts/ZY_helper_scripts/sod_center_food_profile.py", "sod_get_center_food_profile"),
    ("Food consumption", "src/scripts/ZD_centers/center_get_food_consumption.py", "center_get_food_consumption"),
    ("Food store limit", "src/scripts/ZD_centers/center_get_food_store_limit.py", "center_get_food_store_limit"),
    ("Goods consumption", "src/scripts/ZY_helper_scripts/sod_consume_center_trade_goods.py", "script_sod_get_center_food_profile"),
    ("Village food output", "src/scripts/ZY_helper_scripts/sod_village_output_profile.py", ":food_output"),
    ("Village cattle output", "src/scripts/ZY_helper_scripts/sod_village_output_profile.py", ":cattle_output"),
    ("Town market demand", "src/scripts/ZY_helper_scripts/sod_town_market_profile.py", ":consumption_pressure"),
    ("Castle support stores", "src/scripts/ZY_helper_scripts/sod_castle_support_profile.py", ":food_security"),
    ("Population growth", "src/scripts/ZZ_common_array_processing/update_center_population_supply.py", ":food_security"),
    ("Construction labor", "src/scripts/ZY_helper_scripts/sod_population_based_construction.py", ":food_security"),
    ("Security/internal threat", "src/scripts/ZY_helper_scripts/sod_center_security_profile.py", ":food_unrest_pressure"),
    ("Caravan route selection", "src/scripts/ZB_economy_and_trade/cf_select_random_town_at_peace_with_faction_in_trade_route.py", ":food_security"),
    ("Caravan town trade", "src/scripts/ZB_economy_and_trade/do_merchant_town_trade.py", ":food_pressure"),
    ("Field report", "src/scripts/ZY_helper_scripts/sod_store_center_recon_brief_to_s68.py", "Food stores"),
)


def has_token(rel: str, token: str) -> bool:
    return token in (ROOT / rel).read_text(encoding="utf-8")


def main() -> int:
    rows = []
    missing = []
    for label, rel, token in HOOKS:
        ok = has_token(rel, token)
        rows.append("| %s | `%s` | `%s` | %s |" % (label, rel, token, "OK" if ok else "MISSING"))
        if not ok:
            missing.append("%s missing %s" % (rel, token))

    lines = [
        "# Food Reference Audit",
        "",
        "This audit maps food as a real economy input, following the reference direction from `Grain Into Gold`, `Fief`, and the settlement design notes.",
        "",
        "Food is not just flavor: it is a pressure layer that affects health, migration, prosperity, construction labor, unrest, trade demand, caravan routing, and recovery.",
        "",
        "## Core Model",
        "",
        "- Villages create the food base through food output, cattle output, population surplus, land quality, health, prosperity, food security, security, production modifiers, and coercion pressure.",
        "- Towns are net consumers: population, prosperity, craftsmen, visitors, workshops, and services increase consumption and import demand.",
        "- Castles are military consumers: garrisons, prisoners, stores, attached villages, and road control determine endurance and support.",
        "- Caravans should see food scarcity as demand, but unsafe routes and low security reduce willingness to trade.",
        "",
        "## Hook Status",
        "",
        "| Hook | File | Token | Status |",
        "| --- | --- | --- | --- |",
        *rows,
        "",
        "## Food Profile Outputs",
        "",
        "`script_sod_get_center_food_profile` exposes food store, store limit, consumption, days remaining, food security, capacity ratio, food pressure, and food unrest pressure.",
        "",
        "## Reference Checks",
        "",
        "- Food supply affects health and prosperity through trade-good consumption and center recovery paths.",
        "- Food supply affects migration and population growth through weekly population updates.",
        "- Food supply affects construction labor through the population-based construction workforce helper.",
        "- Food supply affects unrest and internal threat through the security profile.",
        "- Food scarcity increases trade demand while low route security reduces trade willingness.",
        "- Cattle remains tied to village condition and output rather than appearing as a detached resource.",
        "",
        "## Next Tuning Questions",
        "",
        "- Should castle military stores distinguish grain/rations from strategic supplies more explicitly?",
        "- Should famine reduce cattle growth before directly harming population?",
        "- Should town luxury/service growth increase food imports faster once population exceeds the ideal band?",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    if missing:
        raise AssertionError("; ".join(missing))
    print("[audit_food_reference] wrote %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
