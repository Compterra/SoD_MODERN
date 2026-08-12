#!/usr/bin/env python3
"""Focused deterministic fixture checks for slot ownership and lifecycle lint."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devkit.slot_lifecycle_lint import slot_lifecycle_lint as lint


STATE_CONTRACTS = {"contract_version": "devkit.campaign-state-contracts.v1", "contracts": []}
OWNERSHIP = {
    "schema": "devkit.slot-lifecycle-ownership.v1",
    "ownership": [
        {
            "id": "fixture-owner",
            "category": "party_slot",
            "slot_names": ["slot_party_fixture_role_alpha"],
            "owner_script_prefixes": ["script_sod_fixture_"],
            "allowed_handoff_scripts": ["script_sod_fixture_handoff"],
            "require_clear": True,
            "clear_values": ["0"],
        }
    ],
}


def write_fixture(root: Path, *, foreign: bool, clear: bool) -> tuple[Path, Path]:
    scripts = root / "src" / "scripts"
    triggers = root / "src" / "triggers"
    scripts.mkdir(parents=True)
    triggers.mkdir(parents=True)
    foreign_block = "(party_set_slot, ':party', slot_party_fixture_role_alpha, 7)," if foreign else ""
    clear_block = "(party_set_slot, ':party', slot_party_fixture_role_alpha, 0)," if clear else ""
    scripts.joinpath("fixture.py").write_text(
        "\n".join(
            (
                "SCRIPTS = [",
                "('sod_fixture_owner', [",
                "  (party_set_slot, ':party', slot_party_fixture_role_alpha, 1),",
                f"  {clear_block}",
                "]),",
                "('sod_foreign_system', [",
                f"  {foreign_block}",
                "]),",
                "]",
            )
        ),
        encoding="utf-8",
    )
    triggers.joinpath("hourly.py").write_text("SIMPLE_TRIGGERS = []\n", encoding="utf-8")
    ownership = root / "ownership.json"
    contracts = root / "contracts.json"
    ownership.write_text(json.dumps(OWNERSHIP), encoding="utf-8")
    contracts.write_text(json.dumps(STATE_CONTRACTS), encoding="utf-8")
    return ownership, contracts


def test_fixture_findings() -> None:
    with tempfile.TemporaryDirectory(prefix="slot-lifecycle-") as temporary:
        root = Path(temporary)
        ownership, contracts = write_fixture(root, foreign=True, clear=False)
        index = lint.build_slot_lifecycle_lint(root, ownership_path=ownership, state_contracts_path=contracts)
        categories = {item["category"] for item in index.findings}
        assert "declared_slot_written_by_unrelated_system" in categories
        assert "declared_lifecycle_slot_never_cleared" in categories
        payload = lint.slot_payload(index, "slot_party_fixture_role_alpha")
        assert payload["slot_count"] == 1

    with tempfile.TemporaryDirectory(prefix="slot-lifecycle-clean-") as temporary:
        root = Path(temporary)
        ownership, contracts = write_fixture(root, foreign=False, clear=True)
        index = lint.build_slot_lifecycle_lint(root, ownership_path=ownership, state_contracts_path=contracts)
        assert not [item for item in index.findings if item["severity"] == "error"]


def test_workspace_catalog() -> None:
    index = lint.build_slot_lifecycle_lint(ROOT)
    summary = lint.summary_payload(index, limit=3)
    assert summary["coverage"]["ownership_rule_count"] >= 1
    ownership = lint.ownership_payload(index, slot="black_khergit")
    assert ownership["rule_count"] >= 1


def main() -> int:
    test_fixture_findings()
    test_workspace_catalog()
    print("[slot_lifecycle_lint] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
