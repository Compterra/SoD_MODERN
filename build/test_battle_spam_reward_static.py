from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def main() -> None:
    rewards = read("src/scripts/ZB_economy_and_trade/party_give_xp_and_gold.py")
    rout = read("src/scripts/ZZ_common_array_processing/rout_check.py")
    objections = read("src/scripts/ZZ_common_array_processing/objectionable_action.py")

    assert_contains(rewards, '(val_max, ":num_player_party_shares", 1)')
    assert_contains(rewards, '(val_clamp, ":stack_gain", 0, 20001)')
    assert_contains(rewards, '(val_clamp, ":total_gain", 0, 20001)')
    assert_contains(rewards, '(val_clamp, ":player_gold_gain", 0, 60001)')
    assert_contains(rewards, '(val_clamp, ":morale_gain", 0, 16)')
    assert_contains(rewards, '(gt, ":morale_gain", 0)')
    assert_not_contains(rewards, '(val_min, ":player_gold_gain", 60000)')
    assert_not_contains(rewards, '(call_script, "script_change_player_party_morale", ":morale_gain"),\n  ]')

    for debug_line in (
        '@Enemy rout check fired: ally cohesion {reg50}, enemy cohesion {reg51}.',
        '@Ally rout check fired: ally cohesion {reg50}, enemy cohesion {reg51}.',
    ):
        idx = rout.index(debug_line)
        window = rout[max(0, idx - 500):idx]
        assert_contains(window, '(eq, "$g_sod_debug", 1)')
        assert_contains(window, '(eq, "$cheat_mode", 1)')

    assert_not_contains(objections, "looks upset")
    assert_contains(objections, "@{s4} takes offense.")
    if objections.index('(try_for_range, ":npc", companions_begin, companions_end)') > objections.index('@{s4} takes offense.'):
        raise AssertionError("Objection display must remain after companion scan setup")
    if objections.index('(try_end),\n\n          (try_begin)') > objections.index('@{s4} takes offense.'):
        raise AssertionError("Objection display should be inside the post-scan single notification block")

    print("test_battle_spam_reward_static: OK")


if __name__ == "__main__":
    main()
