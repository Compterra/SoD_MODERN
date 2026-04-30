# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

import doctor


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    result = doctor.run_doctor(new_only=True)
    law_text = ROOT / "docs" / "reports" / "sod_law_audit_report.txt"
    law_json = ROOT / "docs" / "reports" / "sod_law_faction_snapshot.json"
    assert not result.errors, result.errors
    assert law_text.exists(), "missing sod_law_audit_report.txt"
    assert law_json.exists(), "missing sod_law_faction_snapshot.json"
    raw_text = law_text.read_text(encoding="utf-8")
    assert "faction-owned active laws" in raw_text
    data = json.loads(law_json.read_text(encoding="utf-8"))
    assert len(data["active_law_slots"]) == 10
    assert "sod_law_can_enact_for_faction" in data["diagnostics"]["required_scripts"]
    assert ["sod_law_enfranchisement", "sod_law_serfdom"] in data["diagnostics"]["conflict_pairs"]
    print("test_sod_law_diagnostics: OK")


if __name__ == "__main__":
    main()
