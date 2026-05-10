from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def test_command_dialogue_is_limited_to_external_party_types() -> None:
    start = read("src/dialogs/ZA01_startup_and_dispatch/anyone_start_151.py")

    assert_contains(start, "fac_player_faction")
    assert_contains(start, "slot_party_type, spt_player_mercenaries")
    assert_contains(start, "slot_party_type, spt_player_patrol")
    assert_contains(start, "script_sod_external_party_describe_status_to_s20")
    assert_not_contains(start, '"Yes?"')


def test_external_order_dialogue_uses_shared_helper() -> None:
    order_files = [
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_mate_give_order.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_mate_give_order_02.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_mate_give_order_03.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_mate_give_order_06.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_repeat_for_parties_mate_give_order_details.py",
    ]
    for rel in order_files:
        raw = read(rel)
        assert_contains(raw, "script_sod_external_party_set_order")
        assert_not_contains(raw, "party_set_ai_behavior")
        assert_not_contains(raw, "script_party_set_ai_state")

    helper = read("src/scripts/ZC_parties/sod_external_party_set_order.py")
    assert_contains(helper, "sod_external_order_follow_player")
    assert_contains(helper, "sod_external_order_hold_here")
    assert_contains(helper, "sod_external_order_patrol_here")
    assert_contains(helper, "slot_party_ai_state")
    assert_contains(helper, "slot_party_ai_object")
    assert_contains(helper, "slot_party_follow_me")
    assert_contains(helper, "slot_party_ai_substate")
    assert_contains(helper, "pt_player_patrol")
    assert_contains(helper, "pt_player_patrol_2")


def test_guild_hire_initial_orders_use_named_constants() -> None:
    constants = read("src/constants/module_constants.py")
    spawn = read("src/scripts/ZY_helper_scripts/merc_calculate_hire_quote.py")

    assert_contains(constants, "sod_external_order_follow_player")
    assert_contains(constants, "sod_external_order_hold_here")
    assert_contains(constants, "sod_external_order_patrol_here")

    for rel, token in [
        ("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_hire11.py", "sod_external_order_follow_player"),
        ("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_hire11_02.py", "sod_external_order_hold_here"),
        ("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_hire11_03.py", "sod_external_order_patrol_here"),
    ]:
        raw = read(rel)
        assert_contains(raw, token)
        assert_not_contains(raw, "(assign, \"$temp4\", 1)")
        assert_not_contains(raw, "(assign, \"$temp4\", 2)")
        assert_not_contains(raw, "(assign, \"$temp4\", 3)")

    assert_contains(spawn, "script_sod_external_party_set_order")
    assert_not_contains(spawn, '(eq, ":initial_ai", 1)')
    assert_not_contains(spawn, '(eq, ":initial_ai", 2)')
    assert_not_contains(spawn, '(eq, ":initial_ai", 3)')


def test_contract_and_rejoin_dialogue_are_polished_and_exact_gold_safe() -> None:
    contract = read("src/dialogs/ZZ99_misc_dialogs/anyone_mate_chat_contract.py")
    cancel = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_mate_chat_contract_cancel2.py")
    rejoin_prompt = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_mate_chat_talk_05.py")
    rejoin_ok = read("src/dialogs/ZZ99_misc_dialogs/anyone_mate_chat_rejoin.py")
    ask = read("src/dialogs/ZZ99_misc_dialogs/anyone_mate_give_order_ask.py")

    assert_contains(contract, "Our writ has {reg1} days left")
    assert_contains(contract, "script_sod_external_party_describe_status_to_s20")
    assert_not_contains(contract, '"{reg1} days."')

    assert_contains(cancel, '(ge, ":gold", ":total_cost")')
    assert_not_contains(cancel, '(gt, ":gold", ":total_cost")')

    assert_contains(rejoin_prompt, "Bring the detachment back into my company.")
    assert_contains(rejoin_ok, "fold the detachment back into your column")
    assert_contains(ask, "Give the order")

    for raw in [contract, cancel, rejoin_prompt, rejoin_ok, ask]:
        assert_not_contains(raw, "I want to you")
        assert_not_contains(raw, "Very Well.")
        assert_not_contains(raw, "What do you wish?")


if __name__ == "__main__":
    test_command_dialogue_is_limited_to_external_party_types()
    test_external_order_dialogue_uses_shared_helper()
    test_guild_hire_initial_orders_use_named_constants()
    test_contract_and_rejoin_dialogue_are_polished_and_exact_gold_safe()
    print("test_external_follower_parties_static: OK")
