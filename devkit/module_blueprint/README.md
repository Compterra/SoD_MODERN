# Module Blueprint Compiler

`module_blueprint/` is the DevKit's read-only feature-contract compiler front
end. It gives a coherent feature a stable ID and checks the pieces that the
legacy top-to-bottom module compiler cannot connect on its own:

- canonical modular source fragments and their exact current hashes;
- required Atlas symbols and source anchors;
- deterministic same-area order constraints;
- declared durable-slot ownership rules and AI intent contracts;
- dependency-first impact plans, affected generated/export layers, and focused
  tests that should be run after a reviewed source patch.

The checked-in [`blueprints.json`](blueprints.json) catalog is the source of
truth for these feature contracts. It does **not** generate or rewrite module
source. `src/` remains authoritative, while `compile/` and `_export/` are
reported only as downstream impact.

## LLM-first interface

MCP is the primary interface:

- `blueprint_summary` — catalog coverage and active blocking state.
- `blueprint_find` — locate a feature by a stable ID, source fragment, symbol,
  contract, test, or description.
- `blueprint_explain` — return all exact source/order/ownership/AI/test
  evidence for one feature.
- `blueprint_compile` — make a dependency-first, no-write source impact plan.
- `blueprint_verify` — re-evaluate one feature or the full active catalog.

The deterministic JSON CLI mirrors it:

```powershell
py -3 -B devkit\module_blueprint\module_blueprint.py summary
py -3 -B devkit\module_blueprint\module_blueprint.py find "black khergit"
py -3 -B devkit\module_blueprint\module_blueprint.py explain black-khergit-camped-horde
py -3 -B devkit\module_blueprint\module_blueprint.py compile campaign-dispatch
py -3 -B devkit\module_blueprint\module_blueprint.py verify
```

`./devkit/SoDDev.bat blueprint summary` is a Windows convenience route. It is
not a separate authoring path.

## Contract rules

An active Blueprint must have non-empty `source_fragments`; its paths stay
under `src/`. Required symbols must resolve to exactly one Atlas entity after
any declared `area`/`kind` filter. Source assertions are literal, deliberately
simple anchor checks and must target a source fragment owned by the Blueprint.

Order assertions compare only two sources in the same compiled area. Cross-area
order is not invented because the engine's independent builders do not provide
a meaningful total order. A missing or violated order contract blocks planning.

Slot and AI links point to existing checked-in DevKit contracts. Blocking lint
or AI-contract violations block the feature. Warnings remain visible rather
than being silently approved.

`compile` has no apply mode by design. When a plan is ready, inspect the exact
source/contract evidence, use Change Router or the appropriate semantic editor
to create a SHA-guarded source-only patch, then run `verify` and the listed
focused tests. Never hand-edit `compile/` or `_export/` from a Blueprint plan.
