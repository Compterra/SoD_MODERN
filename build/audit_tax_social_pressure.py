# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "reports" / "tax_social_pressure_audit.md"


CHECKS = (
    ("Realm profile", "src/scripts/ZY_helper_scripts/sod_tax_extraction_profile.py", "sod_get_realm_tax_pressure_profile"),
    ("Center profile", "src/scripts/ZY_helper_scripts/sod_tax_extraction_profile.py", "sod_get_center_tax_extraction_profile"),
    ("Village peasant pressure", "src/scripts/ZY_helper_scripts/sod_village_output_profile.py", "peasant_extraction_pressure"),
    ("Town merchant tariffs", "src/scripts/ZY_helper_scripts/sod_town_market_profile.py", "merchant_tariff_pressure"),
    ("Castle noble obligations", "src/scripts/ZY_helper_scripts/sod_castle_support_profile.py", "noble_obligation_pressure"),
    ("Faith clergy support", "src/scripts/ZY_helper_scripts/sod_faith_system.py", "clergy_faith_support_pressure"),
    ("Law report", "src/scripts/ZZ_common_array_processing/sod_law_reports.py", "Tax social pressure"),
    ("Recon report", "src/scripts/ZD_centers/update_center_recon_notes.py", "Local tax burden"),
)


def has_token(rel: str, token: str) -> bool:
    raw = (ROOT / rel).read_text(encoding="utf-8")
    return token in raw


def main() -> int:
    lines = [
        "# Tax Social Pressure Audit",
        "",
        "This audit checks that taxation is separated into social pressure categories instead of one opaque tax value.",
        "",
        "## Categories",
        "",
        "- Peasant extraction: villages, population retention, food/raw output, farmer reliability, commoner happiness.",
        "- Merchant tariffs: towns, trade volume, liquidity, tariff capture, merchant happiness.",
        "- Noble obligations: castles, scutage reliability, garrison support, noble happiness.",
        "- Clergy/faith support: institutions, faith stability, unrest mitigation, recovery.",
        "- War taxes: emergency revenue with broad unrest, recovery, migration, and happiness pressure.",
        "",
        "## Hook Status",
        "",
        "| Hook | File | Status |",
        "| --- | --- | --- |",
    ]

    failures = []
    for label, rel, token in CHECKS:
        ok = has_token(rel, token)
        status = "OK" if ok else "MISSING"
        lines.append("| %s | `%s` | %s |" % (label, rel, status))
        if not ok:
            failures.append("%s missing %s" % (rel, token))

    lines.extend(
        [
            "",
            "## Profile Outputs",
            "",
            "`script_sod_get_realm_tax_pressure_profile` returns category pressure, total social pressure, revenue, recovery, migration, trade volume, unrest, happiness deltas, and tariff capture.",
            "",
            "## Design Notes",
            "",
            "High taxes remain useful for immediate money, but the pressure is now visible and connected to long-term recovery, migration, liquidity, trade volume, and institutional stability.",
            "",
        ]
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")

    if failures:
        raise AssertionError("; ".join(failures))
    print("[audit_tax_social_pressure] wrote %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
