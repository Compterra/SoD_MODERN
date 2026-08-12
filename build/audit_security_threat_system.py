# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "reports" / "economy_settlements" / "security_threat_system_audit.md"


SECURITY_MODIFIERS = (
    "security_flat",
    "threat_reduction_flat",
    "raid_resistance_pct",
    "bandit_spawn_reduction_pct",
    "desperation_bandit_reduction_pct",
    "warning_range_flat",
    "patrol_response_pct",
    "unrest_flat",
    "unrest_reduction_flat",
)


RUNTIME_HOOKS = (
    ("Security profile", "src/scripts/ZY_helper_scripts/sod_center_security_profile.py"),
    ("Threat compatibility API", "src/scripts/ZD_centers/get_center_threat_level.py"),
    ("Bandit spawn pressure", "src/scripts/ZZ_common_array_processing/spawn_bandits.py"),
    ("Desperation bandit pressure", "src/scripts/ZY_helper_scripts/sod_center_weekly_security_desperation.py"),
    ("Village raid progress and recovery", "src/scripts/ZD_centers/process_village_raids.py"),
    ("Construction workforce", "src/scripts/ZY_helper_scripts/sod_population_based_construction.py"),
    ("Caravan route safety", "src/scripts/ZB_economy_and_trade/cf_select_random_town_at_peace_with_faction_in_trade_route.py"),
    ("Regional threat offers", "src/scripts/ZY_helper_scripts/sod_threat_board_generate_offers.py"),
    ("Regional threat outcomes", "src/scripts/ZY_helper_scripts/sod_threat_board_apply_economy_effect.py"),
    ("Population recovery security", "src/scripts/ZZ_common_array_processing/update_center_population_supply.py"),
    ("Field report builder", "src/scripts/ZY_helper_scripts/sod_store_center_recon_brief_to_s68.py"),
)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def present(path: str, token: str) -> str:
    return "yes" if token in read(path) else "no"


def main() -> int:
    registry = read("src/constants/center_modifier_registry.py")
    buildings = read("src/constants/building_registry.py")

    lines = [
        "# Security Threat System Audit",
        "",
        "## Security Modifier Coverage",
        "",
        "| Modifier | Registered | Building source |",
        "| --- | --- | --- |",
    ]
    for modifier in SECURITY_MODIFIERS:
        lines.append("| `%s` | %s | %s |" % (
            modifier,
            "yes" if '"%s"' % modifier in registry else "no",
            "yes" if '"%s"' % modifier in buildings else "no",
        ))

    lines.extend([
        "",
        "## Runtime Hooks",
        "",
        "| Hook | File | Uses security profile |",
        "| --- | --- | --- |",
    ])
    for label, path in RUNTIME_HOOKS:
        token = "script_sod_get_center_security_profile"
        if label == "Regional threat outcomes":
            token = "script_sod_apply_center_raid_resistance"
        if label == "Population recovery security":
            token = "script_sod_get_center_security_economy_profile"
        lines.append("| %s | `%s` | %s |" % (label, path, present(path, token)))

    lines.extend([
        "",
        "## Design Notes",
        "",
        "- Security is treated as governance and infrastructure: it shapes effective threat, bandit pressure, raid damage, caravan safety, construction labor, and recovery.",
        "- Internal threat comes from starvation, poverty, low health, unrest, and weak local defense even when no enemy party is currently visible.",
        "- Recovery after devastation now reads the security economy profile, so roads, patrols, institutions, and contract companies help damaged centers stabilize.",
    ])

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("[audit_security_threat_system] wrote %s" % REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
