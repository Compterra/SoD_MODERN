from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRS = ("src/dialogs", "src/menus", "src/presentations", "src/scripts", "src/triggers")
CENTRAL = ROOT / "src/scripts/ZB_economy_and_trade/sod_player_charge_gold.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_player_charge_script_clamps_and_reports_payment():
    text = read(CENTRAL)
    assert '(val_max, ":amount", 0)' in text
    assert '(assign, ":paid", 0)' in text
    assert '(ge, ":gold", ":amount")' in text
    assert '(troop_remove_gold, "trp_player", ":paid")' in text
    assert '(assign, reg0, ":paid")' in text
    assert '(assign, reg1, 1)' in text


def test_no_direct_player_gold_removal_outside_charge_script():
    offenders = []
    for rel in SCAN_DIRS:
        for path in (ROOT / rel).rglob("*.py"):
            if path == CENTRAL:
                continue
            text = read(path)
            if '(troop_remove_gold, "trp_player"' in text or '[troop_remove_gold, "trp_player"' in text:
                offenders.append(str(path.relative_to(ROOT)))
    assert offenders == []


def test_known_register_based_payments_use_charge_script():
    checked = {
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_boar_clan_talk_03.py": 'script_sod_player_charge_gold", reg5',
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_boar_clan_recruit_3.py": 'script_sod_player_charge_gold", reg5',
        "src/menus/other/sod_upgrade_continue.py": 'script_sod_player_charge_gold", reg0',
        "src/menus/kingdom/mercenaries_weekly_payment.py": 'script_sod_player_charge_gold", reg1',
    }
    for rel, needle in checked.items():
        assert needle in read(ROOT / rel)


def test_high_risk_paid_outcomes_check_full_payment():
    checked = {
        "src/presentations/0020_sod_fief_management/sod_fief_management.py": [
            '(call_script, "script_sod_player_charge_gold", ":construction_cost")',
            '(eq, reg1, 1)',
            'script_sod_start_center_construction',
        ],
        "src/presentations/0021_sod_royal_artifacts/sod_royal_artifacts.py": [
            '(call_script, "script_sod_player_charge_gold", ":mission_gold")',
            '(eq, reg1, 1)',
            '(party_remove_members , "p_main_party", "$sod_royal_hero", ":mission_heroes")',
        ],
        "src/scripts/ZD_centers/buy_cattle_from_village.py": [
            '(call_script, "script_sod_player_charge_gold", ":cost")',
            '(eq, reg1, 1)',
            '(call_script, "script_game_event_buy_item", "itm_cattle_meat", 0)',
            '(call_script, "script_sod_center_apply_cattle_delta", ":village_no", ":cattle_delta")',
            '(store_mul, ":amount_bought", reg1, -1)',
            '(party_add_members, ":cur_party", "trp_cattle", ":amount_bought")',
        ],
        "src/scripts/ZD_centers/village_recruit_volunteers_recruit.py": [
            '(call_script, "script_sod_player_charge_gold", ":cost")',
            '(eq, reg1, 1)',
            '(party_set_slot, "$current_town", slot_center_volunteer_troop_amount, -1)',
            '(party_add_members, "p_main_party", ":volunteer_troop", ":volunteer_amount")',
        ],
        "src/scripts/ZN_tournaments/tournament_place_bet.py": [
            '(call_script, "script_sod_player_charge_gold", ":bet_amount")',
            '(eq, reg1, 1)',
            '(val_add, "$g_tournament_bet_placed", ":bet_amount")',
        ],
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_mercenary_tavern_talk_hire.py": [
            '(call_script, "script_sod_player_charge_gold", ":total_cost")',
            '(eq, reg1, 1)',
            '(party_add_members, "p_main_party", ":mercenary_troop", "$temp")',
        ],
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_buy_drinks_end.py": [
            '(call_script, "script_sod_player_charge_gold", "$temp")',
            '(eq, reg1, 1)',
            '(call_script, "script_change_player_relation_with_center", "$current_town", 1)',
        ],
        "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_buy_drinks_troops_end.py": [
            '(call_script, "script_sod_player_charge_gold", "$temp")',
            '(eq, reg1, 1)',
            '(call_script, "script_change_player_party_morale", 20)',
        ],
    }
    for rel, needles in checked.items():
        text = read(ROOT / rel)
        positions = [text.index(needle) for needle in needles]
        assert positions == sorted(positions)

