# sod_modern workflow and checkpoint rules

## Source of truth

- Edit modular gameplay content in `src/` first.
- Treat `compile/module_*.py`, `compile/ids/`, `_export/*.txt`, and `docs/reports/*.txt` as generated outputs unless a task explicitly targets legacy non-modular compiler-side files.
- Prefer tracing generated output back to its source fragment or builder instead of hand-editing generated files.

## Build and verification workflow

- Use `build_module.bat` from the repo root as the default build entrypoint.
- For meaningful gameplay, structural, builder, validation, or ordering changes, prefer `build_module.bat --no-cache`.
- After meaningful changes, inspect `docs/reports/doctor_report.txt`.
- Use `compile/module_*.py` only to inspect generated merge output.
- Use `_export/*.txt` only to verify final compiler output.

## Ordered modular files

When adding files to ordered modular domains, update the matching order manifest in the same task:

- `src/menus/_order_game_menus.txt`
- `src/dialogs/_order_dialogs.txt`
- `src/triggers/_order_simple_triggers.txt`
- `src/presentations/_order_presentations.txt`
- `src/mission_templates/_order_mission_templates.txt`
- `src/scripts/ZA_hardcoded_game_scripts/_order_za_scripts.txt`

## Checkpoint-aware working style

Sixth checkpoints are a safety net for this repo. Use them deliberately:

- Before broad refactors, cross-cutting builder edits, or changes affecting many fragments, pause and recognize the current step as a restore point.
- Prefer small, reviewable edits over large blind rewrites so each automatic checkpoint is useful.
- After each file edit or command, review the diff before continuing when the change affects build structure, ordering, or shared preamble logic.
- If a change corrupts generated output or causes Doctor/build failures, restore workspace state to the last known-good checkpoint rather than hand-untangling unrelated breakage.
- Use restore modes intentionally:
  - restore workspace only when code changes are wrong but task context is still useful
  - restore task and workspace when both code and conversational direction need to be rewound
  - restore task only when trying a different prompt strategy while keeping the current code

## Preamble caution

Files under `src/**/_preamble/` affect an entire modular domain. Edit them conservatively, verify imports/helpers carefully, and review diffs immediately after changes.

## Documentation expectations

When the project workflow, builder behavior, Doctor expectations, or team editing conventions change, update the relevant files under `docs/`.
