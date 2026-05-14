# Player Banking System Design

Goal: add a real player-facing banking system for Mount & Blade 1.011, inspired by the Warlords implementation but adapted to this repo's modular source layout, town economy model, and company-account pressure systems.

## Reference

`D:\Program Files (x86)\Steam\steamapps\common\MountBlade Warband\_WORK\SOD_Warlords Latest` has a working banking layer:

- `mnu_bank` town bank menu.
- `go_to_bank` town option gated by `slot_center_has_bank`.
- `trp_bankvault_possessions` as the player bank account container.
- Deposit options for `10000` and `100000` denars.
- Withdraw options for `10000`, `100000`, and all denars.
- `mnu_finance_report` showing cash, bank balance, interest rate, and projected interest.
- `script_ensure_valid_bank_interest_rate`.
- `script_set_bank_interest_rate`.
- Weekly trigger that adds interest to the bank balance and reports the new rate.

Our current repo already has `slot_center_has_bank` and a town `Bank` building, but it is only an economic building. It does not currently provide player deposits, withdrawals, account storage, weekly interest, or a bank menu.

## Design Pillars

- Banks should be useful without replacing risk. Stored denars are safe from some field pressures, but interest should be modest.
- A town bank should feel tied to town prosperity, trade liquidity, merchant happiness, and political stability.
- The system should use modular fragments, not flat Warlords files.
- The first implementation should be simple, stable, and easy to expand.
- Player banking should not silently bypass company-account debt, mercenary pact debt, or serious wage pressure.

## Core Player Features

- Enter a bank from a town that has `slot_center_has_bank`.
- View cash on hand.
- View total bank balance.
- View current weekly interest rate.
- View estimated next weekly interest.
- Deposit fixed amounts.
- Withdraw fixed amounts.
- Withdraw all.
- Optional later: deposit all except a reserve.
- Optional later: named local accounts per town or faction.

## Storage Model

Recommended first pass:

- Add `trp_sod_bankvault_possessions`, inactive hero/merchant-style troop.
- Store the player's total bank balance as that troop's gold.
- This mirrors Warlords and avoids new global overflow issues.

Alternative:

- Use a global, e.g. `$g_sod_player_bank_balance`.
- Simpler to read but less consistent with Warlords and less reusable if later adding inventory-style storage.

Decision: use `trp_sod_bankvault_possessions`.

## Interest Model

Use weekly interest in basis points:

- Store current rate in `$g_sod_bank_interest_rate`.
- Rate is interpreted as `rate / 10000` weekly.
- Example: `80` means `0.8%` weekly.

Suggested range:

- Minimum: `30` = 0.30% weekly.
- Normal: `60` to `100` = 0.60% to 1.00% weekly.
- Maximum: `150` = 1.50% weekly.

Suggested formula:

```text
base random 30..60
+ average town prosperity / 2
+ global trade confidence modifier
- war/disruption modifier
clamp 30..150
```

For a first pass, use:

```text
rate = random 30..60 + average_town_prosperity / 2
clamp 30..150
```

This keeps Warlords' prosperity-linked feel while lowering runaway compounding.

## Weekly Trigger

Add a weekly simple trigger after existing rents/taxes/account updates:

1. Ensure the bank interest rate exists.
2. Store old rate.
3. Recalculate the new weekly rate.
4. Read bank balance from `trp_sod_bankvault_possessions`.
5. If balance > 0, add `balance * old_rate / 10000`.
6. Display a short bank report.

Suggested report:

```text
Bank report: interest {reg1} denars. Balance {reg2} denars. New weekly rate {reg3}/10000.
```

## Menu Flow

Town menu:

- Add `go_to_bank` option near other town services.
- Condition:

```python
(party_slot_eq, "$current_town", slot_center_has_bank, 1)
```

Action:

```python
(jump_to_menu, "mnu_sod_bank")
```

Bank menu:

- Text:

```text
The town bank keeps its ledgers behind heavy shutters. You have {reg1} denars on hand and {reg2} denars deposited. Current weekly interest is {reg3}/10000. Expected next interest: {reg4} denars.
```

Options:

- View finance report.
- Deposit 1,000.
- Deposit 10,000.
- Deposit 100,000.
- Withdraw 1,000.
- Withdraw 10,000.
- Withdraw 100,000.
- Withdraw all.
- Return to town.

Use fixed amounts first. Custom amount entry is not worth the UI complexity in MB 1.011.

## Finance Report

Add `mnu_sod_bank_finance_report`.

Show:

- Cash.
- Bank balance.
- Current weekly rate.
- Projected next interest.
- Company account pressure summary, if available.
- Mercenary pact debt summary, if available.

This is where our version can improve on Warlords: the bank should not exist in isolation from company accounts.

## Debt Integration

First pass:

- Do not block deposits because of ordinary debts.
- Do not auto-pay debts from the bank.
- In finance report, warn when company wage debt or mercenary guild debt exists.

Later expansion:

- Allow paying company arrears from bank balance.
- Allow paying mercenary pact debt from bank balance.
- Let high debt reduce interest or impose fees.
- Let hostile guild debt freeze banking in towns controlled by allied merchants.

## Building Integration

Current bank building already exists:

- `slot_center_has_bank`
- town economic building
- prosperity/population/trade-liquidity modifiers
- manufacture can upgrade from bank

Bank menu should require a built bank. If a town upgrades to manufacture and no longer has `slot_center_has_bank`, decide whether manufacture counts as a bank successor.

Recommendation:

- Treat `slot_center_has_manufacture` as satisfying bank access if it upgrades from bank.
- Add helper script:

```text
script_cf_sod_center_has_bank_service
```

Conditions:

```python
(this_or_next|party_slot_eq, ":center_no", slot_center_has_bank, 1)
(party_slot_eq, ":center_no", slot_center_has_manufacture, 1)
```

## Implemented Files

Constants:

- `src/constants/module_constants.py`
  - ensure `slot_center_has_bank` remains stable

Troops:

- `compile/module_troops.py`
  - `trp_sod_bankvault_possessions`
- `compile/ids/ID_troops.py`
  - tail ID assignment for `trp_sod_bankvault_possessions`

Scripts:

- `src/scripts/ZY_helper_scripts/sod_banking.py`
  - `sod_bank_ensure_valid_interest_rate`
  - `sod_bank_set_interest_rate`
  - `sod_bank_store_report_registers`
  - `sod_bank_deposit`
  - `sod_bank_withdraw`
  - `sod_bank_apply_weekly_interest`
  - `cf_sod_center_has_bank_service`

Menus:

- Town menu fragment:
  - `src/menus/centers/castle/castle_castle.py`
  - `go_to_bank` option in the town services area.
- New menu file:
  - `src/menus/centers/town/sod_bank.py`
  - `mnu_sod_bank`
  - `mnu_sod_bank_finance_report`

Simple triggers:

- `src/triggers/ST04_weekly/entry_0174.py`
  - weekly bank interest trigger under weekly economy/account processing.

Tests:

- `build/test_sod_banking_static.py`

## Static Test Expectations

Test should assert:

- Bank vault troop exists.
- Bank menu exists.
- Town menu has `go_to_bank`.
- Bank menu is gated by `slot_center_has_bank` or helper service script.
- Deposit options remove player gold and add bank vault gold.
- Withdraw options remove bank vault gold and add player gold.
- Interest scripts exist.
- Weekly trigger applies interest to bank vault.
- Finance report includes cash, balance, rate, and interest.

## Implementation Checklist

- [x] Add `trp_sod_bankvault_possessions`.
- [x] Add banking helper scripts.
- [x] Add bank service helper for bank/manufacture access.
- [x] Add town menu option.
- [x] Add bank menu.
- [x] Add finance report.
- [x] Add weekly interest trigger.
- [x] Add static test.
- [x] Regenerate troops, scripts, menus, simple triggers.
- [x] Run focused tests.
- [x] Run `doctor --doctor-new-only`.

## Balancing Notes

Initial suggested values:

- Deposit denominations: `1000`, `10000`, `100000`.
- Withdraw denominations: `1000`, `10000`, `100000`, all.
- Weekly interest: `0.30%` to `1.50%`.
- No fees in first pass.
- No bank failure in first pass.

Later optional risks:

- Towns under siege suspend withdrawals.
- Recently looted towns suspend bank service.
- Very low prosperity reduces rate to minimum.
- Merchant-guild hostility adds fees.
- War or bandit pressure lowers interest.

## Open Questions

- Should bank deposits be global across all bank towns, or local per town?
- Should manufacture count as bank access?
- Should the bank be available only in player-owned towns, all bank towns, or friendly towns?
- Should stored denars be protected from defeat/captivity losses?
- Should the player be allowed to pay company wages directly from the bank?

Recommended first answers:

- Global account.
- Manufacture counts as bank access.
- Any non-hostile town with bank service.
- Bank deposits are protected from battlefield defeat.
- Wages are not auto-paid, but finance report warns about arrears.
