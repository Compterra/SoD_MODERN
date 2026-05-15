from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _block(text: str, start: str, end: str) -> str:
    start_i = text.index(start)
    end_i = text.index(end, start_i)
    return text[start_i:end_i]


def test_wounded_first_pay_does_not_duplicate_full_settlement():
    menu = _read("src/menus/camp/company_accounts.py")
    scripts = _read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    option = _block(menu, '("company_accounts_pay_wounded"', '], "Pay {reg25} denars to wounded first; {reg26} remains."')
    apply = _block(scripts, '(eq, ":choice", sod_company_pay_choice_wounded)', '(else_try),\n     (eq, ":choice", sod_company_pay_choice_delay)')

    assert '(this_or_next|gt, ":wounded", 0)' in option
    assert '(gt, "$g_sod_company_recent_wounded_count", 0)' in option
    assert "(lt, reg25, reg22)" in option
    assert '(val_min, ":intended_payment", ":total_due")' in apply


def test_account_ledger_does_not_offer_event_or_ceremony_actions():
    menu = _read("src/menus/camp/company_accounts.py")
    accounts = menu[: menu.index('("company_rations"')]
    for token in (
        "company_accounts_share_victory_spoils",
        "company_accounts_public_honors",
        "company_accounts_victory_feast",
        "company_accounts_refuse_public_spectacle",
        "company_accounts_casualty_compensation",
        "company_accounts_desertion",
        "company_accounts_mutiny",
        "Share victory spoils",
        "Hold public honors",
        "Pay blood compensation",
        "Handle the active leave request",
        "Review the active mutiny warning",
    ):
        assert token not in accounts


def test_victory_feast_lives_in_recreation_and_consumes_once_after_hard_victory():
    menu = _read("src/menus/camp/company_accounts.py")
    scripts = _read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    option = _block(menu, '("company_recreation_victory_feast"', "],")

    assert '(eq, "$g_sod_company_victory_feast_available", 1)' in option
    assert '(call_script, "script_count_edible_food")' in option
    assert "(ge, reg0, 6)" in option
    assert '(call_script, "script_sod_company_accounts_apply_victory_feast")' in menu
    assert '(assign, "$g_sod_company_victory_feast_available", 0)' in scripts
    assert '(ge, "$g_starting_strength_enemy_party", 1000)' in scripts
    assert '(this_or_next|is_between, "$g_encountered_party", walled_centers_begin, walled_centers_end)' in scripts
    for token in (
        "company_recreation_victory_spoils",
        "company_recreation_public_honor",
        "company_recreation_refuse_spectacle",
        "Pay victory spoils",
        "Stage a public honor",
        "Refuse spectacle",
    ):
        assert token not in menu


def test_spokesperson_menu_keeps_ceremonies_out_of_generic_grievances():
    menu = _read("src/menus/camp/company_spokesperson.py")
    expectations = {
        '("company_spokesperson_rations"': "sod_company_spokesperson_thin_rations",
        '("company_spokesperson_wounded"': "sod_company_spokesperson_wounded_care",
        '("company_spokesperson_offering"': "sod_company_spokesperson_faith_rites",
    }
    for option_id, token in expectations.items():
        option = _block(menu, option_id, "],")
        assert token in option
    for token in (
        "company_spokesperson_honors",
        "company_spokesperson_victory_feast",
        "company_spokesperson_refuse_spectacle",
        "Hold public honors",
        "Hold a victory feast",
        "Refuse spectacle",
    ):
        assert token not in menu
