# Companion Retinue Battle QA

Purpose: verify that companion retinues fight as captain-led internal parties without duplicating troops, erasing survivors, or counting retinue troops against the player's personal party capacity.

## Setup

- Use a save with at least two companions in the main party.
- Give one companion a small retinue with troop types not present in the player party.
- Give another companion a retinue that shares at least one troop type with the player party.
- Fund both command purses and set one to half strength and one to full strength.
- Record each companion's retinue size before battle.

## Ordinary Field Battle

- Start a normal hostile party encounter from the world map.
- Confirm retinue troops appear as allied support when the owning companion is present.
- Win once and lose once.
- After victory, confirm retinue size is equal to pre-battle size minus actual losses, never higher.
- After defeat, confirm retinue survivors are captured/distributed with the defeat outcome and no hidden retinue party remains orphaned.

## Siege Attack

- Attack a walled center while companions are in the party.
- Confirm retinue support does not duplicate the player party roster.
- Resolve the siege and check that retinue parties reattach to the player afterward.
- Confirm wounded/dead losses remain applied to the correct companion retinue.

## Siege Defense

- Defend a center while companions are in the party.
- Confirm retinues are either included safely by the battle bridge or excluded without duplicating.
- After the defense, inspect each retinue report for sensible size, wage, and warning status.

## Village Raid Defense

- Intercept a raid against a village.
- Confirm villagers and retinues can both join as allies without corrupting the battle party list.
- After victory, confirm retinue casualties persist and post-battle freed-troop hiring still happens only after the player exchange screen.

## Ambush Or Quest Battle

- Start a companion quest, ambush, or scripted battle that uses a custom mission template.
- Confirm the mission does not assume `p_main_party` is the only friendly source if retinue support is intended.
- If the mission should be personal or stealth-only, confirm retinue troops do not appear.

## Merge Fallback Check

- Leave `$g_sod_retinue_battle_bridge_force_merge` at `0` for normal play. Hidden allied parties are the default.
- For a controlled debug pass, set `$g_sod_retinue_battle_bridge_force_merge` to `1`.
- Confirm only retinues with troop types absent from the player party use merge fallback.
- Confirm overlapping troop types are skipped rather than merged.
- After battle, confirm fallback restore returns only surviving original retinue troop types to the owning retinue.

## Pass Criteria

- No retinue stack is duplicated after battle.
- No retinue stack disappears unless it was killed, wounded/captured by normal battle handling, discharged by explicit order, or captured during defeat.
- The owning companion remains the visible captain in the player party.
- Retinue parties reattach to `p_main_party` after battle.
- Retinue reports show post-battle size and warnings accurately.
