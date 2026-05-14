from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(haystack: str, needle: str, label: str) -> None:
    if needle not in haystack:
        raise AssertionError(f"{label}: missing {needle!r}")


def main() -> None:
    troop_source = read("compile/module_troops.py")
    troop_ids = read("compile/ids/ID_troops.py")
    scripts = read("src/scripts/ZY_helper_scripts/sod_banking.py")
    town_menu = read("src/menus/centers/castle/castle_castle.py")
    bank_menu = read("src/menus/centers/town/sod_bank.py")
    menu_order = read("src/menus/_order_game_menus.txt")
    trigger = read("src/triggers/ST04_weekly/entry_0174.py")
    trigger_order = read("src/triggers/_order_simple_triggers.txt")

    assert_contains(troop_source, "sod_bankvault_possessions", "bank vault troop source")
    assert_contains(troop_ids, "trp_sod_bankvault_possessions", "bank vault troop id")

    for script_name in (
        "cf_sod_center_has_bank_service",
        "sod_bank_ensure_valid_interest_rate",
        "sod_bank_set_interest_rate",
        "sod_bank_store_report_registers",
        "sod_bank_deposit",
        "sod_bank_deposit_surplus",
        "sod_bank_withdraw",
        "sod_bank_apply_weekly_interest",
    ):
        assert_contains(scripts, script_name, "banking scripts")

    assert_contains(scripts, "slot_center_has_bank", "bank service gate")
    assert_contains(scripts, "slot_center_has_manufacture", "manufacture service gate")
    assert_contains(scripts, "troop_remove_gold, \"trp_player\"", "deposit removes player gold")
    assert_contains(scripts, "troop_add_gold, \"trp_sod_bankvault_possessions\"", "deposit and interest add vault gold")
    assert_contains(scripts, "troop_remove_gold, \"trp_sod_bankvault_possessions\"", "withdraw removes vault gold")
    assert_contains(scripts, "script_troop_add_gold\", \"trp_player\"", "withdraw adds player gold")
    assert_contains(scripts, "player_debt_to_faction", "finance report mercenary debt")
    assert_contains(scripts, "$g_player_debt_to_party_members", "finance report company debt")
    assert_contains(scripts, "will not automatically pay wages or guild debts", "finance report debt warning")

    assert_contains(town_menu, "\"go_to_bank\"", "town bank entry")
    assert_contains(town_menu, "script_cf_sod_center_has_bank_service", "town bank helper gate")
    assert_contains(town_menu, "mnu_sod_bank", "town jumps to bank")

    for option in (
        "sod_bank",
        "sod_bank_finance_report",
        "sod_bank_deposit_1000",
        "sod_bank_deposit_10000",
        "sod_bank_deposit_100000",
        "sod_bank_deposit_surplus_1000",
        "sod_bank_withdraw_1000",
        "sod_bank_withdraw_10000",
        "sod_bank_withdraw_100000",
        "sod_bank_withdraw_all",
    ):
        assert_contains(bank_menu, option, "bank menu")

    assert_contains(menu_order, "centers/town/sod_bank.py", "menu order")
    assert_contains(trigger, "script_sod_bank_apply_weekly_interest", "weekly bank trigger")
    assert_contains(trigger_order, "ST04_weekly/entry_0174.py", "trigger order")


if __name__ == "__main__":
    main()
