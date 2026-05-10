from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def main() -> int:
    dispatcher = read("src/scripts/ZC_parties/decide_kingdom_party_ais.py")
    selector = read(
        "src/dialogs/ZA02_sod_court_and_strategy/"
        "anyone_plyr_repeat_for_troops_marshal_field_marshall_direct2.py"
    )

    if '(neq, ":faction_no", "fac_player_supporters_faction")' in dispatcher:
        raise AssertionError("Player kingdom NPC field marshal is excluded from marshal AI dispatch.")

    assert_contains(dispatcher, '(neq, ":faction_marshall", "trp_player")')
    assert_contains(dispatcher, '(call_script, "script_party_set_ai_state", ":faction_marshall_party", spai_besieging_center, ":faction_ai_object")')
    assert_contains(dispatcher, '(call_script, "script_party_set_ai_state", ":faction_marshall_party", spai_patrolling_around_center, ":faction_ai_object")')
    assert_contains(dispatcher, '(party_set_slot, ":faction_marshall_party", slot_party_commander_party, -1)')
    assert_contains(selector, '(assign, "$g_recalculate_ais", 1)')

    print("[player_field_marshal_ai_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
