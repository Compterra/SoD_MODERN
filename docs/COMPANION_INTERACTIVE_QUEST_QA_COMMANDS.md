# Companion Interactive Quest QA Commands

This is the fast setup guide for live QA of `docs/COMPANION_INTERACTIVE_QUEST_PLAYTEST_MATRIX.md`.

## Enable The QA Menu

The companion interactive quest QA menu is debug-only.

- Set `$g_sod_debug = 1` in the save or through the module's existing debug flow.
- Open camp actions.
- Choose `DEBUG: Companion interactive quest QA.`

The menu is intentionally hidden when `$g_sod_debug` is not enabled.

## Recommended Live QA Flow

Use this sequence for each companion:

1. Make a fresh save before touching the QA menu.
2. Open `DEBUG: Companion interactive quest QA.`
3. Choose `QA: Recruit companion roster and open trust.`
4. Choose the companion's `ready for live climax` option.
5. Return to camp actions.
6. Confirm the appropriate climax action appears, such as `Run Nizar's charge-lane test` or `Guard Artimenner's repair watch`.
7. Save again.
8. Play the climax once as a win and once as a loss/retreat where the mission supports it.
9. Use the companion's `ready for aftermath` option only when testing final moral choices directly.
10. Record pass/fail rows in `docs/COMPANION_INTERACTIVE_QUEST_PLAYTEST_MATRIX.md`.

## What The QA Menu Does

`QA: Recruit companion roster and open trust`:

- Adds missing native companions to the party.
- Sets companion approval high enough for trust-opened content.
- Sets personal quest stage to trust-unlocked.
- Adds a few captives and recruits for Ymira/Lezalit/Bunduk-style checks.

`ready for live climax`:

- Starts the companion's interactive quest if needed.
- Sets the witness/contact/clue state.
- Leaves the confrontation unresolved.
- Unlocks the live mission/menu climax from camp or the relevant world surface.

`ready for aftermath`:

- Starts the companion's interactive quest if needed.
- Sets witness/contact/clue state.
- Marks the confrontation as complete with a neutral-good result grade.
- Unlocks final companion aftermath choices.

## Guardrails

- These hooks require `$g_sod_debug = 1`.
- They are QA accelerators, not replacement quest content.
- They should not be used to mark manual QA complete by themselves; manual QA still requires playing the route in-engine.
- Keep a pre-QA save because the helper intentionally changes companion membership, approval, quest stages, captives, and recruits.

## Companion Climax Shortcuts

- Borcha: ready for road climax.
- Marnid: ready for warehouse climax.
- Ymira: ready for refugee climax.
- Rolf: ready for public proof.
- Baheshtur: ready for rider-oath trial.
- Firentis: ready for restitution climax.
- Deshavi: ready for trail climax.
- Matheld: ready for shield-line test.
- Alayen: ready for standard test.
- Bunduk: ready for watch-line test.
- Katrin: ready for supply watch.
- Jeremus: ready for infirmary crisis.
- Nizar: ready for charge-lane test.
- Lezalit: ready for drill trial.
- Artimenner: ready for repair watch.
- Klethi: ready for alley confrontation.
