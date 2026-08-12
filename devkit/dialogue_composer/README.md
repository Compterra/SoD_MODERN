# Dialogue Composer

Dialogue Composer is a semantic, LLM-first authoring layer for modular
`src/dialogs/**/*.py` fragments. It parses each six-field M&B 1.011 dialogue
entry directly from source, preserves its owning fragment/order, and turns a
route-level action into an exact Change Router patch plan.

It exists because an NPC dialogue state is not a bag of lines: the engine uses
the first matching NPC route. The Composer returns that static ordering hazard
with every route context and patch plan.

## MCP workflow

1. `dialogue_find` returns stable `dialogue:...` route IDs and source/compiled
   order evidence.
2. `dialogue_context` shows first-match/shadow candidates plus Change Router
   source, generated, execution, and test links.
3. `dialogue_patch` plans one semantic operation and returns a unified diff and
   current SHA-256.
4. `dialogue_apply(..., dry_run=true)` rehearses through the shared Change
   Router gate. Set `dry_run=false` only after reviewing the exact diff.
5. `dialogue_verify` checks syntax, ordering/freshness, optional narrow tests
   or isolated build, and repeats static shadow analysis.

For new authored routes, prefer the stricter creation path:

1. `dialogue_create_plan` accepts a checked-in JSON contract with an exact
   source anchor and `before`/`after` placement.
2. It canonicalizes the six M&B route fields, rejects a duplicate
   speaker/input-state/condition signature, and blocks an NPC route after a
   static fallback unless the exact acknowledgement is supplied.
3. `dialogue_create_apply` requires both the source SHA-256 and the exact
   Change Router plan ID from that plan. It is a dry-run unless explicitly
   requested otherwise.

Supported actions are `replace_text`, `set_input_state`, `set_output_state`,
`replace_conditions`, `insert_condition`, `remove_condition`,
`replace_consequences`, `insert_consequence`, `remove_consequence`,
`bridge_menu`, `add_route`, `remove_route`, and `move_route`.

`bridge_menu` requires an `mnu_*` constant and emits the project-native
`(jump_to_menu, "mnu_...")` consequence. Operation-list actions parse their
input as source expressions before planning, so malformed engine operations do
not become a source edit.

The creation request schema is
[`contracts/dialogue-create.v1.schema.json`](contracts/dialogue-create.v1.schema.json).
It deliberately uses JSON arrays for condition and consequence operations;
the Composer never asks an LLM to splice free-form route source.

## Guarantees and boundaries

- A semantic apply delegates to `change_router.apply_source_edits`; it is
  source-only, hash-guarded, atomic, and dry-run by default.
- It never writes `compile/` or `_export/`.
- The Composer does not assume generated dialogue order is fresh. It reports
  when `compile/module_dialogs.py` is older than modular source.
- Shadow findings are static candidates, not a claim that runtime conditions
  are reachable.

## JSON CLI

Run from the module root:

```powershell
py -3 devkit\dialogue_composer\dialogue_composer.py find --input-state bandit_attack
py -3 devkit\dialogue_composer\dialogue_composer.py context "dialogue:src/dialogs/...:L2:C0"
py -3 devkit\dialogue_composer\dialogue_composer.py patch "dialogue:src/dialogs/...:L2:C0" replace_text --value "@New line"
py -3 devkit\dialogue_composer\dialogue_composer.py create-plan --spec-file devkit\output\my-route.json
```

The MCP interface is preferred for structured create specs and operation text.
CLI `apply` remains a dry run unless `--apply` is explicit and the SHA from its
patch plan is supplied. `create-apply` additionally requires the exact
`--expected-plan-id` returned by `create-plan`. On Windows PowerShell,
`--spec-file` avoids native command-line quote stripping; it accepts only a
UTF-8 JSON file inside this module workspace.

## Test

```powershell
py -3 -B devkit\dialogue_composer\test_dialogue_composer.py
```
