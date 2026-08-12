#!/usr/bin/env python3
"""Deterministic fixture and workspace checks for Campaign State Doctor."""

from __future__ import annotations

import json
import tempfile
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devkit.campaign_state_doctor import campaign_state_doctor as doctor


CONTRACT = {
    "contract_version": "devkit.campaign-state-contracts.v1",
    "contracts": [
        {
            "id": "fixture_stationary_camp",
            "kind": "stationary_camp",
            "description": "Fixture stationary-camp invariant.",
            "scope_scripts": [
                "script_fixture_process_day_cycle",
                "script_fixture_refresh_active_parties",
            ],
            "party_template": "pt_fixture_camp",
            "camped_predicate": "script_cf_fixture_party_is_camped",
            "lock_script": "script_fixture_lock_camped_ai",
            "origin_slot": "slot_party_fixture_origin",
            "target_slot": "slot_party_fixture_target",
            "travel_behavior": "ai_bhvr_travel_to_party",
            "relocation_counter": ":days_camped",
            "approach_distance": ":camp_target_dist",
        }
    ],
}


def write_fixture(root: Path, *, broken: bool) -> Path:
    scripts = root / "src" / "scripts"
    triggers = root / "src" / "triggers"
    scripts.mkdir(parents=True)
    triggers.mkdir(parents=True)
    refresh = """
    ("fixture_refresh_active_parties", [
      (try_begin),
        (eq, ":template", "pt_fixture_camp"),
        (call_script, "script_cf_fixture_party_is_camped", ":party_no"),
        (call_script, "script_fixture_lock_camped_ai", ":party_no"),
      (else_try),
        (eq, ":template", "pt_fixture_camp"),
        (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
      (try_end),
    ]),
    """
    if broken:
        refresh = """
    ("fixture_refresh_active_parties", [
      (try_begin),
        (call_script, "script_cf_fixture_party_is_camped", ":party_no"),
        (call_script, "script_fixture_lock_camped_ai", ":party_no"),
      (try_end),
      (party_get_slot, ":camped_origin", ":party_no", slot_party_fixture_origin),
      (try_begin),
        (eq, ":template", "pt_fixture_camp"),
        (le, ":camp_target_dist", 3),
        (eq, ":camped_origin", ":target_center"),
        (eq, ":is_night", 0),
        (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
      (try_end),
    ]),
    """
    source_prefix = textwrap.dedent(
        """\
        SCRIPTS = [
        ("cf_fixture_party_is_camped", [
          (store_script_param, ":party_no", 1),
        ]),
        ("fixture_lock_camped_ai", [
          (store_script_param, ":camp_party", 1),
          (party_set_ai_initiative, ":camp_party", 0),
          (party_set_ai_behavior, ":camp_party", ai_bhvr_hold),
        ]),
        ("fixture_process_day_cycle", [
          (party_get_slot, ":camped_origin", ":camp_party", slot_party_fixture_origin),
          (try_begin),
            (le, ":camp_target_dist", 3),
            (try_begin),
              (ge, ":days_camped", 4),
              (party_set_slot, ":camp_party", slot_party_fixture_origin, 0),
              (party_set_ai_behavior, ":camp_party", ai_bhvr_travel_to_party),
            (else_try),
              (call_script, "script_fixture_lock_camped_ai", ":camp_party"),
            (try_end),
          (else_try),
            (gt, ":camp_target_dist", 3),
            (party_set_ai_behavior, ":camp_party", ai_bhvr_travel_to_party),
          (try_end),
        ]),
        """
    )
    source_text = source_prefix + textwrap.indent(textwrap.dedent(refresh).strip(), "  ") + "\n]\n"
    (scripts / "fixture_horde.py").write_text(source_text, encoding="utf-8")
    (triggers / "hourly.py").write_text(
        textwrap.dedent(
            """
            SIMPLE_TRIGGERS = [
              (1, [
                (call_script, "script_fixture_process_day_cycle"),
              ]),
            ]
            """
        ),
        encoding="utf-8",
    )
    contracts = root / "fixture-contracts.json"
    contracts.write_text(json.dumps(CONTRACT), encoding="utf-8")
    return contracts


def contract_result(index: doctor.StateDoctorIndex) -> dict:
    assert len(index.contract_results) == 1
    return index.contract_results[0]


def test_fixture_contracts() -> None:
    with tempfile.TemporaryDirectory(prefix="campaign-state-doctor-") as temporary:
        root = Path(temporary)
        contracts = write_fixture(root, broken=False)
        index = doctor.build_state_doctor(root, contracts_path=contracts)
        result = contract_result(index)
        assert result["passed"] is True, result
        assert not result["violations"]
        assert index.trigger_paths["script_fixture_process_day_cycle"][0].cadence == "every 1 hour"
        resource = doctor.resource_payload(index, "party_ai_behavior::camp_party:behavior")
        assert resource["resource_count"] == 1
        timeline = doctor.timeline_payload(index, "party_ai_behavior::camp_party:behavior")
        assert timeline["event_count"] >= 3
        assert timeline["trigger_routes"]

    with tempfile.TemporaryDirectory(prefix="campaign-state-doctor-broken-") as temporary:
        root = Path(temporary)
        contracts = write_fixture(root, broken=True)
        index = doctor.build_state_doctor(root, contracts_path=contracts)
        result = contract_result(index)
        assert result["passed"] is False
        assert result["violation_count"] == 1
        violation = result["violations"][0]
        assert violation["category"] == "stationary_camp_movement"
        assert len(violation["counterexample"]) == 3
        findings = doctor.findings_payload(index, severity="error")
        assert findings["finding_count"] == 1


def test_workspace_contract() -> None:
    index = doctor.build_state_doctor(ROOT)
    payload = doctor.summary_payload(index, limit=5)
    assert payload["source"]["script_count"] > 1000
    assert payload["state_model"]["access_count"] > 1000
    contract = doctor.contracts_payload(index, contract_id="black_khergit_camped_ai_stationary")
    assert contract["passed_count"] == 1
    assert contract["failed_count"] == 0
    resource = doctor.resource_payload(index, "slot_party_black_khergit_origin", limit=20)
    assert resource["resource_count"] > 0
    temporal_warnings = [
        finding for finding in index.findings if finding.get("category") == "possible_temporal_ai_overwrite"
    ]
    assert not temporal_warnings, temporal_warnings
    refreshes = [finding for finding in index.findings if finding.get("category") == "explicit_ai_state_refresh"]
    assert len(refreshes) == 1
    assert refreshes[0]["source"]["path"] == "src/scripts/ZI_campaign_ai/sod_hourly_lord_ai_maintenance.py"


def test_party_ai_intent_contracts() -> None:
    contracts_payload = {
        "contract_version": "devkit.campaign-state-contracts.v1",
        "contracts": [
            {
                "id": "fixture-patrol",
                "kind": "party_ai_intent",
                "intent": "patrol",
                "scope_scripts": ["script_fixture_patrol"],
                "expected_behavior": "ai_bhvr_patrol_location",
                "minimum_radius": 3,
                "maximum_radius": 6,
            },
            {
                "id": "fixture-patrol-mismatched-party",
                "kind": "party_ai_intent",
                "intent": "patrol",
                "scope_scripts": ["script_fixture_patrol_mismatch"],
                "expected_behavior": "ai_bhvr_patrol_location",
                "minimum_radius": 3,
                "maximum_radius": 6,
            },
            {
                "id": "fixture-escort",
                "kind": "party_ai_intent",
                "intent": "escort",
                "scope_scripts": ["script_fixture_escort"],
                "attach_to": ":leader",
                "require_detach": True,
            },
            {
                "id": "fixture-raid-return",
                "kind": "party_ai_intent",
                "intent": "raid_return",
                "scope_scripts": ["script_fixture_raid_return"],
                "return_behavior": "ai_bhvr_travel_to_party",
                "return_target": ":camp_party",
                "return_when": ":returning",
            },
            {
                "id": "fixture-despawn",
                "kind": "party_ai_intent",
                "intent": "despawn",
                "scope_scripts": ["script_fixture_despawn"],
                "despawn_when": ":expired",
            },
            {
                "id": "fixture-raid-return-mismatched-party",
                "kind": "party_ai_intent",
                "intent": "raid_return",
                "scope_scripts": ["script_fixture_raid_return_mismatch"],
                "return_behavior": "ai_bhvr_travel_to_party",
                "return_target": ":camp_party",
                "return_when": ":returning",
            },
        ],
    }
    with tempfile.TemporaryDirectory(prefix="campaign-state-intents-") as temporary:
        root = Path(temporary)
        scripts = root / "src" / "scripts"
        triggers = root / "src" / "triggers"
        scripts.mkdir(parents=True)
        triggers.mkdir(parents=True)
        scripts.joinpath("intents.py").write_text(
            textwrap.dedent(
                """
                SCRIPTS = [
                  ("fixture_patrol", [
                    (party_set_ai_behavior, ":party", ai_bhvr_patrol_location),
                    (party_set_ai_patrol_radius, ":party", 4),
                  ]),
                  ("fixture_patrol_mismatch", [
                    (party_set_ai_behavior, ":patrol_a", ai_bhvr_patrol_location),
                    (party_set_ai_patrol_radius, ":patrol_b", 4),
                  ]),
                  ("fixture_escort", [
                    (party_attach_to_party, ":escort", ":leader"),
                    (party_detach, ":escort"),
                  ]),
                  ("fixture_raid_return", [
                    (try_begin),
                      (eq, ":returning", 1),
                      (party_set_ai_behavior, ":raider", ai_bhvr_travel_to_party),
                      (party_set_ai_object, ":raider", ":camp_party"),
                    (try_end),
                  ]),
                  ("fixture_despawn", [
                    (try_begin),
                      (eq, ":expired", 1),
                      (remove_party, ":party"),
                    (try_end),
                  ]),
                  ("fixture_raid_return_mismatch", [
                    (try_begin),
                      (eq, ":returning", 1),
                      (party_set_ai_behavior, ":raider", ai_bhvr_travel_to_party),
                      (party_set_ai_object, ":other_party", ":camp_party"),
                    (try_end),
                  ]),
                ]
                """
            ),
            encoding="utf-8",
        )
        triggers.joinpath("empty.py").write_text("SIMPLE_TRIGGERS = []\n", encoding="utf-8")
        contracts = root / "intent-contracts.json"
        contracts.write_text(json.dumps(contracts_payload), encoding="utf-8")
        index = doctor.build_state_doctor(root, contracts_path=contracts)
        results = {result["id"]: result for result in index.contract_results}
        assert all(
            results[identifier]["passed"]
            for identifier in ("fixture-patrol", "fixture-escort", "fixture-raid-return", "fixture-despawn")
        ), results
        assert results["fixture-patrol-mismatched-party"]["passed"] is False
        assert results["fixture-raid-return-mismatched-party"]["passed"] is False
        assert {result["intent"] for result in results.values()} == {"patrol", "escort", "raid_return", "despawn"}


def test_temporal_overwrite_proofs() -> None:
    """Keep narrow flow proofs from hiding an unguarded real overwrite."""

    with tempfile.TemporaryDirectory(prefix="campaign-state-temporal-") as temporary:
        root = Path(temporary)
        scripts = root / "src" / "scripts"
        triggers = root / "src" / "triggers"
        scripts.mkdir(parents=True)
        triggers.mkdir(parents=True)
        scripts.joinpath("temporal.py").write_text(
            textwrap.dedent(
                """
                SCRIPTS = [
                  ("fixture_guarded_fallback", [
                    (try_begin),
                      (eq, ":route", 1),
                      (call_script, "script_party_set_ai_state", ":party", spai_patrolling_around_center, ":center"),
                      (assign, ":deployed", 1),
                    (try_end),
                    (try_begin),
                      (eq, ":deployed", 0),
                      (call_script, "script_party_set_ai_state", ":party", spai_holding_center, ":fallback_center"),
                    (try_end),
                  ]),
                  ("fixture_spawn_rebind", [
                    (spawn_around_party, ":origin", "pt_fixture"),
                    (assign, ":new_party", reg0),
                    (call_script, "script_party_set_ai_state", ":new_party", spai_patrolling_around_center, ":origin"),
                    (spawn_around_party, ":other_origin", "pt_fixture"),
                    (assign, ":new_party", reg0),
                    (call_script, "script_party_set_ai_state", ":new_party", spai_holding_center, ":other_origin"),
                  ]),
                  ("fixture_explicit_refresh", [
                    (call_script, "script_party_set_ai_state", ":party", spai_undefined, -1),
                    (call_script, "script_party_set_ai_state", ":party", spai_besieging_center, ":center"),
                  ]),
                  ("fixture_real_conflict", [
                    (call_script, "script_party_set_ai_state", ":party", spai_patrolling_around_center, ":center"),
                    (call_script, "script_party_set_ai_state", ":party", spai_holding_center, ":fallback_center"),
                  ]),
                ]
                """
            ),
            encoding="utf-8",
        )
        triggers.joinpath("empty.py").write_text("SIMPLE_TRIGGERS = []\n", encoding="utf-8")
        contracts = root / "contracts.json"
        contracts.write_text(json.dumps({"contract_version": "devkit.campaign-state-contracts.v1", "contracts": []}), encoding="utf-8")

        index = doctor.build_state_doctor(root, contracts_path=contracts)
        overwrite_warnings = [
            finding for finding in index.findings if finding.get("category") == "possible_temporal_ai_overwrite"
        ]
        assert len(overwrite_warnings) == 1, overwrite_warnings
        assert "script_fixture_real_conflict" in overwrite_warnings[0]["summary"]
        refreshes = [finding for finding in index.findings if finding.get("category") == "explicit_ai_state_refresh"]
        assert len(refreshes) == 1, refreshes
        assert "script_fixture_explicit_refresh" in refreshes[0]["summary"]


def main() -> int:
    test_fixture_contracts()
    test_workspace_contract()
    test_party_ai_intent_contracts()
    test_temporal_overwrite_proofs()
    print("[campaign_state_doctor] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
