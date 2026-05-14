# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(raw: str, needle: str) -> None:
    if needle not in raw:
        raise AssertionError(f"Missing expected token: {needle}")


def main() -> int:
    scripts = read("src/scripts/ZY_helper_scripts/sod_company_accounts.py")
    menus = read("src/menus/camp/company_accounts.py")

    assert_contains(scripts, "$g_sod_company_desertion_pending_confrontation")
    assert_contains(scripts, 'jump_to_menu, "mnu_company_desertion_confrontation"')
    assert_contains(scripts, "sod_company_accounts_describe_desertion_confrontation_to_s40")
    assert_contains(scripts, "have come before you rather than slipping away in the dark")
    assert_contains(scripts, "service without faith becomes bitterness")
    assert_contains(scripts, "honor is not kept by rotting under a strained banner")
    assert_contains(scripts, "our term has become arrears and promises")

    assert_contains(menus, '("company_desertion_confrontation"')
    assert_contains(menus, "script_sod_company_accounts_describe_desertion_confrontation_to_s40")
    for option_id in (
        "company_desertion_confront_paid",
        "company_desertion_confront_persuade",
        "company_desertion_confront_battle_promise",
        "company_desertion_confront_unpaid",
        "company_desertion_confront_forbid",
    ):
        assert_contains(menus, option_id)
    for response in (
        "sod_company_desertion_response_paid",
        "sod_company_desertion_response_persuade",
        "sod_company_desertion_response_battle_promise",
        "sod_company_desertion_response_unpaid",
        "sod_company_desertion_response_forbid",
    ):
        assert_contains(menus, f"script_sod_company_accounts_resolve_desertion\", {response}")

    if menus.index('("company_desertion_confrontation"') < menus.index('("company_desertion_petition"'):
        raise AssertionError("Confrontation menu should live after the account-facing petition menu")

    print("[company_desertion_confrontation_static] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
