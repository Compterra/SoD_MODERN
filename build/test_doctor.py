# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import doctor


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _make_repo() -> Path:
    root = Path(tempfile.mkdtemp(prefix="doctor-test-"))
    _write(root / "src" / "scripts" / "ok.py", 'SCRIPTS = [("ok", [(assign, reg0, 1)])]\n')
    _write(root / "src" / "menus" / "_order_game_menus.txt", "menu_ok.py\n")
    _write(root / "src" / "menus" / "menu_ok.py", 'MENUS = [("menu_ok",0,"ok","none",[],[("continue",[], "Done", [(jump_to_menu, "mnu_menu_ok")])])]\n')
    _write(root / "src" / "dialogs" / "_order_dialogs.txt", "D1 dlg_ok.py\n")
    _write(root / "src" / "dialogs" / "dlg_ok.py", 'DIALOGS = [[anyone,"start",[],"Hi","close_window",[(assign, reg0, 1)]]]\n')
    _write(root / "src" / "triggers" / "_order_simple_triggers.txt", "t_ok.py\n")
    _write(root / "src" / "triggers" / "t_ok.py", "SIMPLE_TRIGGERS = [(24, [], [(assign, reg0, 1)])]\n")
    _write(root / "src" / "presentations" / "_order_presentations.txt", "p_ok.py\n")
    _write(root / "src" / "presentations" / "p_ok.py", 'PRESENTATIONS = [("prsnt_ok", 0, "mesh", [(ti_on_presentation_load, [(assign, reg0, 1)])])]\n')
    _write(root / "src" / "mission_templates" / "_order_mission_templates.txt", "mt_ok.py\n")
    _write(root / "src" / "mission_templates" / "mt_ok.py", 'MISSION_TEMPLATES = [("mt_ok", 0, 0, "ok", [], [(1, 0, ti_once, [], [(assign, reg0, 1)])])]\n')
    _write(root / "src" / "constants" / "_order_constants.txt", "core.py\n")
    _write(root / "src" / "constants" / "core.py", "slot_foo = 1\n")
    _write(root / "src" / "quests" / "q_ok.py", "# noop\n")
    _write(root / "compile" / "ids" / "ID_troops.py", "trp_player = 0\n")
    _write(root / "compile" / "ids" / "ID_items.py", "itm_test = 0\n")
    _write(root / "compile" / "ids" / "ID_factions.py", "fac_test = 0\n")
    _write(root / "compile" / "ids" / "ID_parties.py", "p_test = 0\n")
    _write(root / "compile" / "ids" / "ID_party_templates.py", "pt_test = 0\n")
    _write(root / "compile" / "ids" / "ID_quests.py", "qst_test = 0\n")
    _write(root / "compile" / "ids" / "ID_scenes.py", "scn_test = 0\n")
    return root


def _run_in_repo(root: Path, **kwargs) -> doctor.DoctorResult:
    old_root = doctor.ROOT
    old_report = doctor.REPORT_PATH
    old_report_json = doctor.REPORT_JSON_PATH
    old_docs_dir = doctor.DOCS_DIR
    old_docs_edit = doctor.DOCS_EDIT
    old_docs_reports = doctor.DOCS_REPORTS
    old_src_root = doctor.SRC_ROOT
    old_paths = {
        "SRC_SCRIPTS": doctor.SRC_SCRIPTS,
        "SRC_MENUS": doctor.SRC_MENUS,
        "SRC_DIALOGS": doctor.SRC_DIALOGS,
        "SRC_TRIGGERS": doctor.SRC_TRIGGERS,
        "SRC_PRESENTATIONS": doctor.SRC_PRESENTATIONS,
        "SRC_MISSION_TEMPLATES": doctor.SRC_MISSION_TEMPLATES,
        "SRC_CONSTANTS": doctor.SRC_CONSTANTS,
        "SRC_QUESTS": doctor.SRC_QUESTS,
        "ORDER_DIALOGS": doctor.ORDER_DIALOGS,
        "ORDER_TRIGGERS": doctor.ORDER_TRIGGERS,
        "ORDER_MENUS": doctor.ORDER_MENUS,
        "ORDER_PRESENTATIONS": doctor.ORDER_PRESENTATIONS,
        "ORDER_MISSION_TEMPLATES": doctor.ORDER_MISSION_TEMPLATES,
        "ORDER_CONSTANTS": doctor.ORDER_CONSTANTS,
        "ORDER_ZA": doctor.ORDER_ZA,
        "ALLOWLIST_GLOBALS_PATH": doctor.ALLOWLIST_GLOBALS_PATH,
        "ALLOWLIST_DUPLICATE_IDS_PATH": doctor.ALLOWLIST_DUPLICATE_IDS_PATH,
        "ALLOWLIST_COST_PATH": doctor.ALLOWLIST_COST_PATH,
        "ALLOWLIST_NONASCII_PATH": doctor.ALLOWLIST_NONASCII_PATH,
        "ALLOWLIST_FORBIDDEN_PATTERNS_PATH": doctor.ALLOWLIST_FORBIDDEN_PATTERNS_PATH,
        "ALLOWLIST_STUBS_PATH": doctor.ALLOWLIST_STUBS_PATH,
        "ALLOWLIST_DIALOG_DUPES_PATH": doctor.ALLOWLIST_DIALOG_DUPES_PATH,
        "BASELINE_FINDINGS_PATH": doctor.BASELINE_FINDINGS_PATH,
    }
    try:
        doctor.ROOT = root
        doctor.DOCS_DIR = root / "docs"
        doctor.DOCS_EDIT = doctor.DOCS_DIR / "edit"
        doctor.DOCS_REPORTS = doctor.DOCS_DIR / "reports"
        doctor.REPORT_PATH = doctor.DOCS_REPORTS / "doctor_report.txt"
        doctor.REPORT_JSON_PATH = doctor.DOCS_REPORTS / "doctor_report.json"
        doctor.SRC_ROOT = root / "src"
        doctor.SRC_SCRIPTS = root / "src" / "scripts"
        doctor.SRC_MENUS = root / "src" / "menus"
        doctor.SRC_DIALOGS = root / "src" / "dialogs"
        doctor.SRC_TRIGGERS = root / "src" / "triggers"
        doctor.SRC_PRESENTATIONS = root / "src" / "presentations"
        doctor.SRC_MISSION_TEMPLATES = root / "src" / "mission_templates"
        doctor.SRC_CONSTANTS = root / "src" / "constants"
        doctor.SRC_QUESTS = root / "src" / "quests"
        doctor.ORDER_DIALOGS = doctor.SRC_DIALOGS / "_order_dialogs.txt"
        doctor.ORDER_TRIGGERS = doctor.SRC_TRIGGERS / "_order_simple_triggers.txt"
        doctor.ORDER_MENUS = doctor.SRC_MENUS / "_order_game_menus.txt"
        doctor.ORDER_PRESENTATIONS = doctor.SRC_PRESENTATIONS / "_order_presentations.txt"
        doctor.ORDER_MISSION_TEMPLATES = doctor.SRC_MISSION_TEMPLATES / "_order_mission_templates.txt"
        doctor.ORDER_CONSTANTS = doctor.SRC_CONSTANTS / "_order_constants.txt"
        doctor.ORDER_ZA = doctor.SRC_SCRIPTS / "ZA_hardcoded_game_scripts" / "_order_za_scripts.txt"
        doctor.ALLOWLIST_GLOBALS_PATH = doctor.DOCS_EDIT / "doctor_allowlist_globals.txt"
        doctor.ALLOWLIST_DUPLICATE_IDS_PATH = doctor.DOCS_EDIT / "doctor_allowlist_duplicate_ids.txt"
        doctor.ALLOWLIST_COST_PATH = doctor.DOCS_EDIT / "doctor_allowlist_missing_cost.txt"
        doctor.ALLOWLIST_NONASCII_PATH = doctor.DOCS_EDIT / "doctor_allowlist_non_ascii.txt"
        doctor.ALLOWLIST_FORBIDDEN_PATTERNS_PATH = doctor.DOCS_EDIT / "doctor_allowlist_forbidden_patterns.txt"
        doctor.ALLOWLIST_STUBS_PATH = doctor.DOCS_EDIT / "doctor_allowlist_stubs.txt"
        doctor.ALLOWLIST_DIALOG_DUPES_PATH = doctor.DOCS_EDIT / "doctor_allowlist_dialog_duplicates.txt"
        doctor.BASELINE_FINDINGS_PATH = doctor.DOCS_EDIT / "doctor_baseline_findings.txt"
        kwargs.setdefault("check_feature_integrations", False)
        kwargs.setdefault("check_refs", False)
        return doctor.run_doctor(**kwargs)
    finally:
        doctor.ROOT = old_root
        doctor.REPORT_PATH = old_report
        doctor.REPORT_JSON_PATH = old_report_json
        doctor.DOCS_DIR = old_docs_dir
        doctor.DOCS_EDIT = old_docs_edit
        doctor.DOCS_REPORTS = old_docs_reports
        doctor.SRC_ROOT = old_src_root
        for key, value in old_paths.items():
            setattr(doctor, key, value)


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(msg)


def main() -> None:
    root = _make_repo()

    res = _run_in_repo(root)
    _assert(not res.errors, "healthy repo should not produce errors")
    report_json_path = root / "docs" / "reports" / "doctor_report.json"
    _assert(report_json_path.exists(), "json report missing")
    report_json = json.loads(report_json_path.read_text(encoding="utf-8"))
    _assert("slowest_timings" in report_json, "json report missing slowest timings")
    _assert("report_artifacts" in report_json, "json report missing report artifacts")
    _assert(any(item.get("name") == "doctor_report.txt" for item in report_json["report_artifacts"]), "report artifacts missing text report")
    _assert("stub_detection_scripts" in res.timings_ms, "timings missing")

    _write(root / "src" / "scripts" / "stub_empty.py", 'SCRIPTS = [("x", [])]\n')
    res = _run_in_repo(root)
    _assert(any("[STUB]" in w for w in res.warnings), "stub warning not detected")
    _assert(not res.errors, "warn mode should not error on stub-only repo")

    res = _run_in_repo(root, stubs_strict=True)
    _assert(any("[STUB]" in e for e in res.errors), "strict stub mode should error")

    _write(root / "src" / "dialogs" / "dlg_dup_02.py", 'DIALOGS = [[anyone,"start",[],"Hi","close_window",[(assign, reg0, 1)]]]\n')
    _write(root / "src" / "dialogs" / "_order_dialogs.txt", "D1 dlg_ok.py\nD2 dlg_dup_02.py\n")
    res = _run_in_repo(root)
    _assert(any("[DIALOG-DUP]" in w for w in res.warnings), "dialog dup warning missing")

    _write(root / "docs" / "edit" / "doctor_baseline_findings.txt", "[dialog-dup] *\n")
    res = _run_in_repo(root, new_only=True)
    _assert(not any("[DIALOG-DUP]" in w for w in res.warnings), "baseline should suppress dup warning")

    res = _run_in_repo(root, strict_all=True)
    _assert(res.errors and not res.warnings, "strict umbrella should promote warnings to errors")

    print("[test_doctor] OK")


if __name__ == "__main__":
    main()
