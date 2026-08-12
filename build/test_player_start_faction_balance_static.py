from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from devkit.troop_item_balance import troop_item_balance as balance


def require(text: str, token: str) -> None:
    assert token in text, f"Missing player-start faction balance contract: {token}"


def main() -> None:
    activation = (ROOT / "src/scripts/ZF_factions/activate_deactivate_player_faction.py").read_text(encoding="utf-8", errors="replace")
    templates = (ROOT / "compile/module_party_templates.py").read_text(encoding="utf-8", errors="replace")
    require(activation, 'slot_faction_reinforcements_a, "pt_sod_5_reinforcements_b"')
    require(activation, 'slot_faction_reinforcements_b, "pt_sod_5_reinforcements_a"')
    require(templates, '(trp_sod_ant_elite,1,2)')
    require(templates, '(trp_sod_ant_trained_javelinman,2,4)')
    require(templates, '(trp_sod_mar_trained_crossbowman,2,5)')
    require(templates, '(trp_sod_mar_elite_crossbowman,1,4)')
    require(templates, '(trp_sod_zer_3_cavalry,0,2)')
    require(templates, '(trp_sod_zer_1_noble,0,2)')

    profile = balance.balance_player_start_factions(balance.build_balance_index(ROOT))
    assert profile["state"] == "within_static_balance_targets"
    assert profile["player_start_culture_count"] == 5
    assert all(contract["status"] == "present" for contract in profile["source_contracts"])
    assert all(spread["within_target"] for spread in profile["pressure_spreads"].values())
    assert all(spread["target_max_ratio"] == 1.35 for spread in profile["pressure_spreads"].values())
    zerrikanian = next(culture for culture in profile["cultures"] if culture["culture"]["id"] == "zerrikanian")
    assert zerrikanian["activation_binding"]["template_codes"] == {
        "a": "sod_5_reinforcements_b",
        "b": "sod_5_reinforcements_a",
        "c": "sod_5_reinforcements_c",
    }
    print("test_player_start_faction_balance_static: OK")


if __name__ == "__main__":
    main()
