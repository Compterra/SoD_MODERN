# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIALOG_ROOT = ROOT / "src" / "dialogs"

BUILTIN_TERMINALS = {
    "close_window",
    "start",
    "member_talk",
    "party_encounter_hostile_defender",
    "party_encounter_lord_hostile_attacker",
    "party_encounter_lord_hostile_attacker_2",
    "party_encounter_lord_hostile_attacker_2_surrender",
    "party_encounter_hostile_ultimatum_surrender",
    "defeat_lord_answer",
    "defeat_lord_answer_1",
    "cpdla_defeat_lord_answer",
    "cpsq_0",
}

IMPERIAL_PREFIXES = (
    "cp_",
    "cpsq_",
    "cpdla_",
    "cpdla1_",
    "cpdla2_",
    "cpehus_",
    "pelha2s_",
    "pelha2f_",
    "cc_humilitae_",
    "capitalist_avoid_battle_",
    "centurion_avoid_battle",
    "legate_",
)

DIALOG_RE = re.compile(
    r"\[\s*([^,\[]+?)\s*,\s*"
    r"\"([^\"]+)\"\s*,\s*"
    r"\[(.*?)\]\s*,\s*"
    r"\"(?:\\.|[^\"])*\"\s*,\s*"
    r"\"([^\"]+)\"",
    re.DOTALL,
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_imperial_dialog(path: Path, raw: str, state: str, target: str) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if any(part in rel for part in ("legate", "centurion")):
        return True
    if any(state.startswith(prefix) or target.startswith(prefix) for prefix in IMPERIAL_PREFIXES):
        return True
    if "slot_troop_centurion_personality" in raw or "trp_kingdom_6_lord" in raw:
        return True
    return False


def main() -> int:
    states = {}
    target_refs = []
    suspicious_preclose = []

    for path in sorted(DIALOG_ROOT.rglob("*.py")):
        raw = read(path)
        for match in DIALOG_RE.finditer(raw):
            speaker, state, conditions, target = match.groups()
            if not is_imperial_dialog(path, raw, state, target):
                continue

            states.setdefault(state, []).append(path)
            target_refs.append((path, state, target))

            pre_target_block = raw[: match.end()]
            if target != "close_window" and "script_kill_kingdom_hero" in pre_target_block:
                suspicious_preclose.append((path, state, target))

    missing = []
    for path, state, target in target_refs:
        if target in BUILTIN_TERMINALS:
            continue
        if target not in states:
            missing.append((path, state, target))

    if missing:
        print("Missing Imperial dialog targets:")
        for path, state, target in missing:
            print(f"  {path.relative_to(ROOT)}: {state} -> {target}")

    if suspicious_preclose:
        print("Risky kill-before-advance Imperial dialog lines:")
        for path, state, target in suspicious_preclose:
            print(f"  {path.relative_to(ROOT)}: {state} -> {target}")

    print(
        "[audit_imperial_dialogs] "
        f"states={len(states)} refs={len(target_refs)} missing={len(missing)} risky_kill={len(suspicious_preclose)}"
    )
    return 1 if missing or suspicious_preclose else 0


if __name__ == "__main__":
    raise SystemExit(main())
