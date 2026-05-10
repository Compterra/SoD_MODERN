# Training Cadence Design

This document records the anti-exploit training cadence pass. The design goal is simple: training should feel like repeated drills over time, not a midnight spell that turns last-minute recruits into veterans.

## Problem

The classic Trainer behavior rewards troops present at the daily tick. That creates an exploit:

- Recruit low-tier troops just before the daily training pulse.
- Let the party's Trainer skill apply a full day of XP immediately.
- Upgrade many troops after almost no time under command.

This is especially visible with farmers, recruits, freed captives, and other low-tier stacks.

## Preferred Rule

Training should be split into four smaller pulses:

- Fire every 6 hours.
- Apply roughly one quarter of the old daily training XP each pulse.
- Report training as recent drill activity rather than a single midnight event.

This means a troop recruited just before a tick receives only one 6-hour slice, not a full day.

## Current Source Reality

The editable module source exposes several SoD-controlled training systems:

- Player-owned center trainers.
- Companion retinue training.
- NPC lord/garrison XP growth.
- Training-ground practice rewards.

The native player-party Trainer pulse does not appear as editable module-source logic in this repository. It appears to be engine-side or otherwise not present in the generated source files. A full anti-exploit fix for the main party therefore needs a later replacement strategy, such as disabling or offsetting the native effect if the engine allows it, or adding stack-age eligibility around a custom Trainer system.

The compiled skill definition still describes the native behavior:

```text
Every day, each hero with this skill adds some experience to every other member of the party whose level is lower than his/hers.
Experience gained goes as: {0,4,10,16,23,30,38,46,55,65,80}.
```

That description should not be changed until the main-party Trainer behavior is actually replaced. Otherwise the UI would claim a 6-hour cadence while the player party still receives the native daily pulse.

## Implemented First Pass

- [x] Player-owned center trainers now run every 6 hours instead of every 24 hours.
- [x] Center trainer XP per pulse is quartered by removing the old daily `* 4` multiplier.
- [x] Companion retinue training now checks every 6 hours instead of every 24 hours.
- [x] Companion retinue training XP is divided by 4 per pulse.
- [x] Companion retinue reports now describe `last drill` XP instead of `training last day` XP.
- [x] Static coverage verifies the exposed cadence changes.

## Not Yet Solved

- [ ] Native main-party Trainer pulse still needs an engine-safe audit/fix.
- [ ] Main-party troop stack age is not tracked.
- [ ] Garrison transfers into the main party are not yet training-age gated.
- [ ] Prisoner recruitment into the main party is not yet training-age gated.
- [ ] Freed-captive additions into the main party are not yet training-age gated.
- [ ] Quest reward troops are not yet training-age gated.

## Recommended Next Step

Implement a custom main-party Trainer replacement only after confirming whether the native Trainer pulse can be disabled, intercepted, or safely counterbalanced.

Before implementing a custom main-party replacement, answer these questions in code or test notes:

- Can the native daily Trainer effect be disabled by skill flags, engine behavior, or module configuration?
- If not, can the native effect be detected and counterbalanced without corrupting troop stack XP?
- Can troop stack age be tracked without breaking stack merges?
- Should fresh troops become eligible after one 6-hour interval or after a full day?
- Should garrison, prisoner, freed-captive, retinue, and quest-reward transfers share the same eligibility rule?

If it can be replaced:

- Add `script_sod_apply_player_party_training_interval`.
- Run it every 6 hours.
- Use Trainer skill from player and eligible companions.
- Apply XP only to troops lower level than each trainer.
- Divide classic daily XP by 4.
- Track newly joined stack counts or use a simpler "eligible after next interval" policy.
- Add a daily summary report rather than four spammy reports.

If it cannot be replaced:

- Keep SoD-controlled training smoothed.
- Avoid adding extra main-party training that stacks with native Trainer.
- Consider reducing exploit pressure through recruitment timing, upgrade delay, or training eligibility flags where stack tracking is safe.

## Static Test Checklist

- [x] Assert center trainer trigger runs every 6 hours.
- [x] Assert center trainer trigger no longer multiplies trainers by 4.
- [x] Assert companion retinue training requires only 6 hours since last drill.
- [x] Assert companion retinue XP is divided by 4 per pulse.
- [x] Assert retinue report text says `last drill`.
- [x] Assert the design doc records the native main-party Trainer limitation.
- [x] Assert the compiled Trainer skill still documents the native daily behavior.
- [x] Assert no custom main-party Trainer interval script has been added on top of native Trainer.

## Manual QA Checklist

- [ ] Add trainers to a player-owned center and verify garrison upgrades can occur across the day.
- [ ] Verify center trainers do not train four times too strongly.
- [ ] Give a companion a retinue and Trainer skill, then verify training can happen every 6 hours.
- [ ] Verify companion retinue training reports show last drill XP.
- [ ] Verify fresh main-party recruits still receive native Trainer behavior until the later main-party replacement pass.
