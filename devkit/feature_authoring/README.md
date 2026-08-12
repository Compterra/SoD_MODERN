# Feature Authoring Compiler

The Feature Authoring Compiler is the DevKit's LLM-first front door for a coherent M&B 1.011 feature. It connects the existing Module Blueprint Compiler, Module Atlas, Dialogue Composer, Presentation Layout Composer, Order Control, and Change Router instead of creating a separate source editor.

It answers four questions deterministically:

1. Which real engine entrypoints own this feature?
2. Where do those entrypoints sit in the module system's order-sensitive source?
3. What exact source diff would a typed feature change create?
4. Which declared contracts and focused tests must still hold afterward?

## Simple workflow

```powershell
SoDDev.bat feature summary
SoDDev.bat feature explain --feature-id campaign-dispatch
SoDDev.bat feature plan --feature-id campaign-dispatch
SoDDev.bat feature verify --feature-id campaign-dispatch --run-tests
```

For a new change, send the MCP `feature_plan` tool an inline Feature Intent JSON object. It is always no-write. Select one returned `change_id`, review its unified diff, then call `feature_apply` with:

- the exact `feature_plan_id`;
- that change's `base_sha256`;
- `dry_run: true` first.

`feature_apply` deliberately writes only one named modular source target at a time. A feature can span scripts, menus, dialogue, triggers, and presentations, but M&B source assembly is order-sensitive and a multi-file write is not honestly transactional. Re-plan siblings after each non-dry apply.

## Engine entrypoints

`entrypoints.json` is a checked-in policy catalog. The registry is built from the actual workspace, not a hand-maintained duplicate list. It currently covers:

- hardcoded `game_*` engine callbacks;
- module scripts;
- simple campaign triggers;
- menus;
- dialogue input states;
- presentations;
- mission templates and mission callback blocks;
- quests; and
- constants / generated-ID evidence.

Use `entrypoint_find` and `entrypoint_explain` before authoring. Each entrypoint has static source provenance, modular order, generated-ID evidence where relevant, and a bounded specialist trace.

## Typed operation IR

Feature changes never accept a raw Python tuple or expression string. Operations use JSON:

```json
{
  "op": "call_script",
  "args": [
    {"reference": "script_sod_report_record_event"},
    {"local": "category"},
    1
  ]
}
```

Typed operands make intent explicit:

- `{"symbol": "assign"}` emits a bare imported symbol;
- `{"reference": "script_example"}` emits a quoted module ID;
- `{"local": "value"}` and `{"global": "g_value"}` emit `":value"` and `"$g_value"`;
- `{"register": "s68"}` emits a bare M&B register;
- `{"string": "@Text"}` emits a quoted literal;
- `{"list": [...]}`, `{"tuple": [...]}`, and `{"combine":{"operator":"or","items":[...]}}` compose only safe expressions.

Use `feature_ir_render` / `SoDDev.bat feature ir-render` to inspect the rendered M&B source before planning.

## Feature Intent

The schema is [`contracts/feature-intent.v1.schema.json`](contracts/feature-intent.v1.schema.json). The checked-in catalog is [`features.json`](features.json). A minimal intent is:

```json
{
  "schema": "sod-modern.feature-intent.v1",
  "id": "example-feature",
  "title": "Example Feature",
  "status": "draft",
  "description": "Owns one bounded module-system behavior.",
  "blueprint_id": "example-feature",
  "entrypoints": ["entrypoint:script:example_anchor"],
  "changes": [],
  "verification": {
    "tests": ["build/test_example_feature.py"],
    "require_blueprint": true
  }
}
```

Supported typed change families are `module`, `dialogue`, and `presentation`. They compile into the existing specialist semantic actions, so dialogue retains first-match analysis and presentation retains overlay/register analysis. Destructive removal and cross-fragment reordering remain intentionally in their dedicated Atlas / Dialogue / Order workflows, which contain the necessary migration and ordering safeguards.

## Semantic baselines

`feature_semantic_snapshot` returns an in-memory JSON baseline (it writes nothing). Pass that object to `feature_semantic_diff` after a source edit to report changed entrypoint provenance, order, generated IDs, Blueprint state, and typed plan bases. Use the existing workspace-wide `semantic_change_snapshot` / `semantic_change_diff` tools when the impact is broader than one feature.

## Safety boundary

- Planning, registry queries, snapshots, traces, and verification are read-only.
- Applying requires both the reviewed feature plan ID and the current source SHA-256.
- Apply defaults to a dry run.
- Only canonical `src/` fragments can be written.
- `compile/` and `_export/` are never written by this compiler.
- A reviewed normal build remains the step that refreshes generated module files and exports.
