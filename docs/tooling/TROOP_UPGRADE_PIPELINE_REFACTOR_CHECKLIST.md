# Troop Upgrade Pipeline Refactor Checklist

## Summary

This checklist tracks the SoD troop upgrade pipeline refactor for Mount & Blade 1.011. The goal is to keep existing player-facing upgrade menus stable while making AI lord troop upgrades reliable, especially when lord parties gain XP while roaming away from a walled center.

## Current Pipeline

- [x] Document XP sources:
  - [x] 48-hour AI lord and garrison training XP through `script_sod_party_process_hero_and_garrison_training_xp`.
  - [x] Battle simulation XP through `script_cf_party_upgrade_with_xp`.
  - [x] Lord party creation XP through `script_create_kingdom_hero_party`.
  - [x] Mercenary maintenance, contract, preview, and spawn XP through existing mercenary helpers.
- [x] Document the upgrade resolver: `script_cf_party_upgrade_with_xp`.
- [x] Document the center permission gate: `script_sod_troop_can_upgrade_at_center`.
- [x] Document the cost gate: `script_sod_get_cost_to_upgrade_troop_at`.
- [x] Document player-facing callers: camp upgrades, town upgrades, marshal upgrades, and garrison upgrades.

## Compatibility Requirements

- [x] Preserve `script_cf_party_upgrade_with_xp` as the public entrypoint.
- [x] Preserve existing callers that pass extra ignored parameters.
- [x] Preserve `reg0` and `reg1` behavior for upgrade permission checks.
- [x] Do not rename `slot_troop_sod_upgrade1`, `slot_troop_sod_upgrade2`, `slot_troop_sod_soldier`, or `slot_troop_sod_upgrades`.
- [x] Keep player-facing upgrade menus on center-specific permission checks.
- [x] Keep legacy non-lord party upgrade context stable unless a later audit proves it should change.

## Refactor Implementation

- [x] Split `script_cf_party_upgrade_with_xp` into named responsibilities:
  - [x] `script_sod_party_upgrade_context_to_regs` resolves source party, leader, faction, center context, gold pool, leader-wealth tracking, artifact bias, and mobile-training-center use.
  - [x] `script_sod_party_upgrade_find_ai_training_center_to_reg` resolves fallback AI training centers.
  - [x] `script_sod_party_upgrade_stack_paths_to_regs` resolves upgrade1/upgrade2 targets and split counts.
  - [x] `script_sod_party_upgrade_path_allowed_to_reg` centralizes path permission checks.
  - [x] `script_sod_party_upgrade_apply_elite_cap_to_reg` centralizes faith and noble caps.
  - [x] `script_sod_party_upgrade_apply_path_to_regs` applies one upgrade path and returns the updated gold pool.
- [x] Remove duplicated upgrade1 and upgrade2 cost/permission/cap/application blocks.
- [x] Keep temp-party mutation so source stack iteration remains stable.
- [x] Commit leader wealth changes only after all stack upgrade attempts complete.

## Mobile AI Lord Upgrade Fix

- [x] Add mobile AI lord fallback training-center selection.
- [x] If a kingdom hero party is attached to a walled center, use that center as before.
- [x] If a kingdom hero party is roaming, select a fallback training center in this order:
  - [x] Lord-owned walled center, not under siege.
  - [x] Faction central center, if walled, faction-owned, and not under siege.
  - [x] Any faction-owned walled center, not under siege.
- [x] If no valid center exists, allow only no-center-safe upgrades supported by the permission gate.
- [x] Never route player menu upgrade checks through the mobile AI fallback context.

## Permission Gate Refinements

- [x] Keep `script_sod_troop_can_upgrade_at_center` as the center-specific permission source.
- [x] Preserve facility checks for barracks, range, stables, chapter, temple, and chapel.
- [x] Preserve faction and original-faction permission checks.
- [x] Preserve mercenary guild hall exceptions.
- [x] Preserve blocked troop ranges and looter/native exceptions.
- [x] Preserve no-center mercenary/guild upgrade behavior.

## Diagnostics And Maintainability

- [x] Add comments naming why mobile AI gets fallback training-center context.
- [x] Add debug-only reporting when a kingdom hero party has no safe training center.
- [x] Add a debug-only AI upgrade report for attempts, skips, context, and gold spent.
- [x] Add static guard coverage so duplicated upgrade1/upgrade2 blocks do not return.
- [ ] Future balancing: review AI upgrade gold pools, faith-roll odds, and noble caps after playtesting.
- [x] Future polish: add a debug report summarizing AI upgrade attempts, skipped center requirements, and gold spent.

## Validation

- [x] Add `build/test_troop_upgrade_pipeline_static.py`.
- [x] Run `py build\test_troop_upgrade_pipeline_static.py`.
- [x] Run `py build\test_sod_upgrade_menu_text_static.py`.
- [x] Run `py build\test_castle_mercenary_guild_static.py`.
- [x] Run `py build\test_faith_ascension_gates.py`.
- [x] Run `py build\test_training_cadence_static.py`.
- [x] Run `py build\test_mercenary_market_static.py`.
- [x] Run `py build\build_all.py --no-cache`.
- [x] Confirm doctor reports 0 warnings.
- [x] Confirm slot verification reports 0 warnings and 0 errors.
- [x] Confirm generated compile import check is OK.
- [x] Confirm no live `_export/*.txt` diffs unless explicitly intended.
