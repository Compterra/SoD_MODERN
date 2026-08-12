from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_ai_mercenary_contract_dialogue_uses_live_role_and_target() -> None:
    description = read(
        "src/scripts/ZY_helper_scripts/sod_merc_market_describe_ai_contract_to_s68.py"
    )
    player_prompt = read(
        "src/dialogs/ZD01_encounters_battles_and_prisoners/"
        "anyone_plyr_party_encounter_mercs_contract.py"
    )
    response = read(
        "src/dialogs/ZD01_encounters_battles_and_prisoners/"
        "anyone_party_encounter_mercs_contract.py"
    )
    deployment = read("src/scripts/ZY_helper_scripts/sod_merc_market_deploy_ai_contract.py")
    order = read("src/dialogs/_order_dialogs.txt")

    for token in (
        '"sod_merc_market_describe_ai_contract_to_s68"',
        "slot_party_sod_merc_contract_role",
        "slot_party_sod_merc_contract_employer",
        "slot_party_ai_object",
        "sod_merc_contract_role_patrol",
        "sod_merc_contract_role_garrison_support",
        "sod_merc_contract_role_supply_column",
        "sod_merc_contract_role_field_company",
        "sod_merc_contract_role_escort",
        "sod_merc_contract_role_mercenary_lord",
        "sod_merc_contract_role_special_world_activity",
        "str_store_party_name, s70, \":target_center\"",
        "(assign, reg0, 0)",
        "(assign, reg0, 1)",
    ):
        assert_contains(description, token)

    assert_contains(player_prompt, "spt_ai_mercenaries")
    assert_contains(player_prompt, "What work are you doing?")
    assert_contains(player_prompt, "script_sod_merc_market_describe_ai_contract_to_s68")
    assert_contains(response, '"party_encounter_mercs_contract"')
    assert_contains(response, '"{s68}"')
    assert_contains(response, "script_sod_merc_market_describe_ai_contract_to_s68")

    # Escort, mercenary-lord, and special jobs retain their live role while
    # following an employer. Only a missing deployment falls back to field service.
    for role in (
        "sod_merc_contract_role_escort",
        "sod_merc_contract_role_mercenary_lord",
        "sod_merc_contract_role_special_world_activity",
    ):
        assert_contains(deployment, role)
    assert_contains(deployment, "Mobile jobs have no center target")
    assert_contains(deployment, "orphaned mobile job becomes field service")

    prompt_path = (
        "ZD01_encounters_battles_and_prisoners/"
        "anyone_plyr_party_encounter_mercs_contract.py"
    )
    response_path = (
        "ZD01_encounters_battles_and_prisoners/"
        "anyone_party_encounter_mercs_contract.py"
    )
    assert order.index(
        "ZD01_encounters_battles_and_prisoners/anyone_plyr_party_encounter_mercs.py"
    ) < order.index(prompt_path)
    assert order.index(prompt_path) < order.index(
        "ZD01_encounters_battles_and_prisoners/anyone_plyr_party_encounter_mercs_02.py"
    )
    assert order.index(response_path) < order.index(
        "ZA01_startup_and_dispatch/trp_khergit_chieftain_start.py"
    )
