# SoD Modern DevKit MCP Server

This is the primary interface for an LLM or Codex client. It exposes structured
diagnostics plus semantic and raw source-only guarded edit operations over
local STDIO; there is no dashboard or interactive UI requirement.

## Capabilities

| Tool | Agent use |
| --- | --- |
| `devkit_catalog` | Discover the checked-in tool catalog and contract. |
| `devkit_health` | Confirm generated inputs/exports and freshness before analysis. |
| `dialogue_summary` | Find state inventory, ordering hazards, and string-placeholder risks. |
| `dialogue_routes` | Inspect exact engine evaluation order with source provenance. |
| `dialogue_entry` | Fetch one stable, one-based compiled route. |
| `dialogue_model_summary` | Summarize proof-oriented branch-free dialogue reachability analysis and its model boundaries. |
| `dialogue_model_findings` | Filter proved route contradictions, first-match shadows, overlaps, ambiguous choices, and dead states. |
| `dialogue_model_state` | Inspect exact compiled precedence and proof status for one state. |
| `dialogue_model_route` | Explain one route's normalized supported constraints, group position, and related findings. |
| `dialogue_composer_summary` | Summarize semantic authored-route coverage and compiled-order mapping. |
| `dialogue_find` | Find modular routes and return stable route IDs plus source/compiled-order evidence. |
| `dialogue_context` | Inspect a route's static first-match hazards and linked source/runtime context. |
| `dialogue_create_plan` | Plan one canonical new route from an anchored JSON contract; reject duplicates and unacknowledged NPC shadow risks. |
| `dialogue_create_apply` | Rehearse or apply exactly that reviewed creation plan using both source-SHA and plan-ID guards. |
| `dialogue_patch` | Plan semantic text/state/condition/consequence/menu/route edits without writing source. |
| `dialogue_apply` | Rehearse or apply a semantic dialogue edit through the shared source-only SHA gate. |
| `dialogue_verify` | Verify semantic dialogue work with static first-match analysis. |
| `string_trace` | Follow a phrase, ID, or register across source, generated, and export layers. |
| `string_integrity` | Preflight text sinks and s-register flow before changing a source fragment. |
| `text_export_parity` | Replay the legacy processor path in temporary staging and compare text-bearing exports without writing live data. |
| `rgl_log_analyze` | Parse a real M&B gameplay log, cluster engine-error cascades, map script evidence through source/generated/export layers, classify warnings, and optionally identify a stale live module deployment. |
| `rgl_log_contract` | Check protected engine-callback dynamic-party guards before a build or release. |
| `release_gate` | Run the strict isolated source/generated/all-export release preflight; it blocks on staged compiler diagnostics, unapproved blank string sinks, dialogue-model errors, order/ID regressions, and protected engine callback party-handle regressions without writing live data. |
| `blueprint_summary` | Summarize checked-in feature contracts and their active source/symbol/order/slot/AI/test state. |
| `blueprint_find` | Locate a stable feature Blueprint by source, semantic symbol, contract, test, or description. |
| `blueprint_explain` | Return a feature's exact source ownership, Atlas entities, order proof, external contracts, and focused tests. |
| `blueprint_compile` | Produce a dependency-first no-write source impact plan; it deliberately has no apply mode. |
| `blueprint_verify` | Re-evaluate a feature or the active Blueprint catalog after a reviewed source edit. |
| `feature_summary` | Summarize Feature Intents and the source-derived engine-entrypoint registry. |
| `feature_find` | Find a checked-in Feature Intent by feature, Blueprint, entrypoint, or focused-test evidence. |
| `entrypoint_find` | Find real callbacks, scripts, triggers, menus, dialogue states, presentations, missions, quests, and constants. |
| `entrypoint_explain` | Return bounded source/order/ID and static execution evidence for one real engine entrypoint. |
| `feature_explain` | Explain an inline or checked-in Feature Intent through entrypoints, Blueprint evidence, and typed-change validation. |
| `feature_intent_validate` | Validate typed Feature Intent JSON and reject raw Python tuple/expression escapes. |
| `feature_ir_render` | Render typed operation JSON to safe M&B source syntax without writing source. |
| `feature_plan` | Produce independently reviewable typed source patch plans, bounded traces, and verification obligations. |
| `feature_apply` | Rehearse or apply one reviewed source change using both feature-plan-ID and source-SHA guards. |
| `feature_verify` | Re-check Feature Intent contracts, source syntax/order/freshness, and optional focused tests. |
| `feature_semantic_snapshot` | Capture an in-memory per-feature semantic baseline without an artifact write. |
| `feature_semantic_diff` | Compare entrypoint provenance/order/IDs, Blueprint state, and typed patch bases to a prior feature snapshot. |
| `content_forge_summary` | Summarize typed content packs across dialogue, quest/event, campaign AI, troop/item, and presentation slices. |
| `content_pack_find` | Find a pack by its brief, lore/tone/acceptance criteria, slice, entrypoint, contract, or verification evidence. |
| `content_pack_explain` | Explain a checked-in or inline content pack through its brief, typed slices, entrypoints, and scenario declarations. |
| `content_pack_validate` | Validate strict Content Pack JSON and specialist route/test/Blueprint/scenario prerequisites without writing. |
| `content_pack_compile` | Compile a pack to an explicit order-aware sequence of specialist changes without writing. |
| `content_pack_plan` | Produce exact source/balance diffs, SHA guards, AI evidence, order impacts, and verification obligations. |
| `content_pack_preview` | Return narrative, campaign AI, balance, presentation-canvas, and review-canvas preview evidence. |
| `content_pack_review` | Return a structured/Mermaid human review canvas backed by the exact typed plan. |
| `content_pack_apply` | Rehearse or apply one reviewed content change with a content-plan ID and current SHA; troop/item changes also require Balance Lab plan SHA. |
| `content_pack_verify` | Re-check specialist source/order evidence, AI contracts, optional tests/staged checks, and bounded scenarios. |
| `content_pack_snapshot` | Capture an in-memory pack semantic baseline without an artifact write. |
| `content_pack_semantic_diff` | Compare pack contract, source/balance plan bases, and AI intent evidence to a prior snapshot. |
| `content_pack_catalog_plan` | Validate and plan one strict create/replacement of a checked-in Content Forge pack contract; returns only the `packs.json` diff and catalog SHA guard. |
| `content_pack_catalog_apply` | Rehearse or save one reviewed strict pack contract to `devkit/content_forge/packs.json`; real save also requires `SAVE CONTENT PACK`. |
| `campaign_state_summary` | Build a temporal source model of campaign state readers/writers, trigger paths, contracts, and bounded overwrite findings. |
| `campaign_state_findings` | Filter possible state collisions and contract violations with compact counterexample evidence. |
| `campaign_state_resource` | Find every source-mapped reader/writer of a party AI field, slot, lifecycle field, or global. |
| `campaign_state_timeline` | Inspect full branch/order evidence and known trigger routes for one state resource. |
| `campaign_state_contracts` | Evaluate checked-in gameplay invariants before an in-game surprise reveals a silent behavior defect. |
| `campaign_ai_intents` | Inspect stationary, patrol, escort, raid-return, and despawn contracts with source evidence. |
| `slot_lifecycle_summary` | Summarize declared durable-slot owners, clear lifecycles, handoffs, and sharing candidates. |
| `slot_lifecycle_findings` | Filter owner violations, missing clear failures, and read-after-clear candidates. |
| `slot_lifecycle_ownership` | Review exact slot/prefix ownership declarations and approved handoffs. |
| `slot_lifecycle_slot` | Trace all readers/writers and owner evidence for a durable slot. |
| `campaign_scenario_summary` | Summarize safe campaign-state generation and supported literal script execution. |
| `campaign_scenario_catalog` | List checked-in state domains, entry scripts, and assertions. |
| `campaign_scenario_fuzz` | Run seeded valid-state fuzzing and return a counterexample or an honest inconclusive boundary. |
| `text_explain` | Explain a text sink through conditions, register writers, scripts, globals, menu transitions, and provenance. |
| `register_history` | Trace generated reads and writes of a register, local, or global across execution contexts. |
| `possible_texts` | Enumerate bounded static templates and substitution candidates for matching sinks. |
| `string_provenance_summary` | Summarize literal script-call coverage for interprocedural `s`-register writers. |
| `string_provenance_paths` | Follow one register through nested literal calls and branch evidence. |
| `string_provenance_explain` | Resolve a visible text sink's script-clobber risk into actual paths/boundaries. |
| `semantic_change_snapshot` | Capture the behavioral surface; a named snapshot writes only an ignored DevKit baseline. |
| `semantic_change_diff` | Compare semantic dialogue/state/text/ID/trigger/export effects with a named baseline. |
| `presentation_layout_summary` | Summarize static presentation/overlay layout coverage and model boundaries. |
| `presentation_find` | Find presentations and direct overlay bindings with stable IDs. |
| `presentation_canvas` | Build a bounded static canvas with estimated layout and binding findings. |
| `presentation_preview` | Write a diagnostic SVG only beneath `devkit/output/`. |
| `presentation_patch` | Plan semantic overlay/content/control edits without writing source. |
| `presentation_apply` | Rehearse or apply a semantic layout edit through the shared source-only SHA gate. |
| `presentation_verify` | Verify semantic layout work with static canvas and build evidence. |
| `module_atlas_summary` | Summarize the complete semantic index across all eight modular source areas. |
| `module_integrity` | Detect duplicate authored definitions, actual unresolved direct references, syntax errors, and known generated-ID fallback boundaries. |
| `module_find` | Find a constant, route, menu/option, mission/trigger, presentation, quest, script, or simple trigger by semantic evidence. |
| `module_context` | Retrieve one Atlas entity's exact ownership, operation blocks, children, links, source/generated context, and supported semantic actions. |
| `module_graph` | Traverse a bounded static cross-area dependency graph from an Atlas entity ID. |
| `menu_flow` | Inspect a menu's authored options, operations, and static outgoing flow. |
| `script_flow` | Inspect one script's operations and static dependency/call graph. |
| `mission_timeline` | Inspect one mission template's event/timed trigger timeline and outbound dependencies. |
| `trigger_timeline` | Inspect simple trigger intervals, operations, and static outbound links. |
| `quest_registry` | List authored quests with direct inbound/outbound static link counts. |
| `entity_references` | Trace an authored definition and its direct semantic plus bounded raw-source references. |
| `module_patch` | Plan semantic constant/menu/mission/quest/script/simple-trigger edits without writing source. |
| `module_apply` | Rehearse or apply a reviewed Module Atlas semantic edit through the shared source-only SHA gate. |
| `module_verify` | Verify an Atlas semantic edit with syntax, ordering, freshness, test, and isolated-build evidence. |
| `order_summary` | Summarize explicit source manifests, authored/compiled order, generated IDs, and protected engine-order contracts. |
| `order_map` | Return bounded source-fragment, entity, generated-marker, or ID-table order evidence. |
| `order_explain` | Explain one order-sensitive source/entity/route/ID target and its safe move boundary. |
| `order_risk` | Assess projected first-match, generated-ID, and protected-prefix risk before an anchored move. |
| `order_plan_move` | Produce a reviewed anchored manifest/dialogue diff and current SHA apply contract. |
| `order_apply_move` | Rehearse or apply one guarded order move; defaults to dry-run and never writes generated/export layers. |
| `order_contracts` | Evaluate strict manifests, hardcoded legacy menu IDs, and engine callback order contracts. |
| `order_baseline` | Write a confined DevKit snapshot of source fragment order and generated ID tables. |
| `order_diff` | Compare current order with a baseline and elevate generated engine callback-ID shifts. |
| `order_verify` | Run protected contracts, source/generated marker parity, dialogue-order hazards, and optional baseline drift. |
| `balance_summary` | Confirm legacy troop/item authoring authority, evaluated coverage, balance dimensions, and ID parity. |
| `balance_find_items` | Find evaluated items by text/type/shop availability/score with direct source provenance. |
| `balance_item` | Inspect decoded bit-packed stats, price/score relationship, editable constructors, and troop users. |
| `balance_find_troops` | Find evaluated troops by code/name/faction/role/level with static kit pressure. |
| `balance_troop` | Inspect one troop's stats, random inventory pool, kit band, source record, and direct upgrades. |
| `balance_upgrade_tree` | Traverse bounded explicit `upgrade()` / `upgrade2()` declarations with balance evidence. |
| `balance_compare` | Compare two through eight exact troop/item records using normalized evaluated fields. |
| `balance_outliers` | Surface bounded static item value/power and troop kit/upgrade review candidates. |
| `balance_patch` | Produce a record-local legacy-authoring balance diff, source SHA, and plan SHA without writing. |
| `balance_apply` | Rehearse or explicitly apply one reviewed direct troop/item record patch; dry-run is default. |
| `balance_verify` | Verify source evaluation, direct inventory/upgrade integrity, hardwired IDs, and ID-table parity without building. |
| `workbench_summary` | Summarize the CBO-inspired M&B Workbench, its contracts, scenarios, and fixed evidence workflow. |
| `workbench_doctor` | Check Workbench prerequisites and checked-in catalogs without building or mutating module data. |
| `workbench_impact` | Build one compact cross-tool ownership/impact/coverage/next-step packet from an ID, source target, or query. |
| `workbench_scope_check` | Run a fixed fast/standard/deep validation profile for one exact Atlas entity. |
| `workbench_text_lint` | Preflight visible text and string/register risks with static source/generated provenance. |
| `workbench_order_report` | Run the fixed protected-order, parity, dialogue-hazard, and optional baseline-drift packet. |
| `workbench_contract_drift` | Evaluate declarative static contracts and expose active blockers. |
| `workbench_contract_baseline` | Write an explicit confined static-observation baseline artifact. |
| `workbench_coverage` | Report exact contract/scenario/test/generated coverage maturity for authored entities. |
| `workbench_scenarios` | List checked-in fixed evidence scenarios and their runtime-proof boundaries. |
| `workbench_scenario_run` | Run only a registered builtin/test scenario; never an arbitrary command. |
| `workbench_release_readiness` | Build an honest static/manual release checklist without certifying gameplay. |
| `workbench_draft` | Create a disabled DevKit-only authoring packet without activating module content. |
| `change_router_summary` | Summarize the persistent source/generated/order link index. |
| `code_find` | Find code/text and return stable source target IDs. |
| `linked_context` | Retrieve source ownership, generated links, execution links, and test candidates. |
| `change_impact` | Establish linked downstream risk before editing a source fragment. |
| `patch_plan` | Produce a source-only unified diff plus the required SHA-256 apply guard. |
| `apply_source_edits` | Explicitly apply a SHA-guarded source patch; dry-run is the default. |
| `verify_change` | Verify syntax, order, freshness, tests, and optional isolated staging build. |
| `dialogue_graph` | Return structured state edges and optional DOT. |
| `workspace_audit` | Map the complete source, generated, export, ordering, freshness, and validation topology before diagnosis. |

Every successful or failed tool result follows
[`tool-result.v1.schema.json`](../contracts/tool-result.v1.schema.json). The
server never mutates generated modules, exports, or Codex settings.
`dialogue_apply`, `dialogue_create_apply`, `presentation_apply`, `module_apply`, and `apply_source_edits` share the
same Change Router source mutation gate: each is dry-run by default, requires
the current SHA from its plan, and writes only an exact `src/**/*.py` target.
The semantic tools do not bypass the raw safety mechanism. Module Atlas
authoring intentionally routes dialogue and presentation records to their
dedicated semantic composers. `presentation_preview` is a confined
`devkit/output/*.svg` diagnostic artifact write.

Order Control is intentionally narrower than a generic sorter. It can move
only two source fragments governed by the same declared `_order*.txt` manifest
or two dialogue routes in one source fragment. Fragment applies write that one
manifest line only; dialogue applies delegate to the existing semantic
Dialogue Composer path. `order_baseline` writes only an ignored
`devkit/order_control/baselines/` artifact. Order Control never renames a
section folder, hand-edits generated IDs, builds the module, or writes
`compile/` / `_export/`. A non-dry move touching an active protected
engine/legacy contract additionally requires the explicit
`allow_protected_contract_change=true` override after review.

The Balance Lab is intentionally a separate compatibility gate rather than a
back door around Change Router. In this workspace `compile/module_items.py`
and `compile/module_troops.py` are legacy authoring inputs consumed by the
M&B 1.011 processors, not generated exports. `balance_patch` can only change
bounded fields on a direct record and always returns a unified diff, current
source SHA, and plan SHA. `balance_apply` is dry-run by default; a non-dry
apply requires both SHA values and
`allow_legacy_compile_authoring=true`. A hardwired record additionally
requires `allow_protected_legacy_record_change=true`. It never adds/moves a
record, edits `compile/ids`, writes generated layers, or overwrites `_export`.
After a real apply, use the ordinary reviewed build and inspect generated ID
and export diffs before in-game smoke testing the changed shop/loadout/upgrade
path.

Module Blueprint Compiler is a feature-contract front end, not an alternate
legacy compiler. Its checked-in catalog declares which canonical `src/`
fragments, Atlas symbols, same-area order boundaries, slot owners, AI intent
contracts, and focused tests constitute one coherent feature. `blueprint_compile`
reports the dependency-first source/generated/export impact but never writes
anything; when its state is ready, use the relevant semantic editor or Change
Router to make a separately reviewed SHA-guarded source-only patch.

Feature Authoring Compiler is the corresponding LLM-first orchestration layer,
not a second source editor. Start with `feature_summary`, then use
`entrypoint_find` / `entrypoint_explain` to map the actual M&B engine surfaces
before sending a typed Feature Intent to `feature_plan`. Its operation IR has
no raw Python tuple or expression field; scripts, dialogue, and presentation
changes are rendered and then revalidated by their existing semantic
specialists. A feature can span many fragments, but `feature_apply` is
deliberately one named source target at a time: it requires the exact reviewed
feature-plan ID and current SHA, defaults to dry-run, and never writes
`compile/` or `_export/`. Follow a non-dry apply with `feature_verify` and a
separately reviewed build. See [`../feature_authoring/README.md`](../feature_authoring/README.md).

The Workbench follows the same boundary: `workbench_impact`,
`workbench_scope_check`, contracts, coverage, scenarios, text lint, and
release-readiness are source-read-only and use only fixed local checks.
`workbench_contract_baseline` and `workbench_draft` are intentional artifact
writes under ignored `devkit/workbench/` folders; neither can activate content
or alter `src/`, `compile/`, or `_export/`.

`semantic_change_snapshot` is the matching cross-slice review gate: without a
label it is read-only; with a reviewed label it writes only
`devkit/semantic_change_diff/baselines/`. Run it before a source edit, then
run `semantic_change_diff` after the normal reviewed build. It never writes
source, generated modules, or exports.

Content Forge is the higher-level authored-content layer. Start with
`content_forge_summary`, then use `content_pack_explain` to bind a creative
brief, lore/tone constraints, and acceptance criteria to real engine
entrypoints. Its slices delegate typed changes to Feature Authoring, Dialogue
Composer, Presentation Layout, and Balance Lab rather than opening a raw
source writer. `content_pack_plan` returns exact diffs and specialist SHA
contracts; `content_pack_review` returns a structured/Mermaid review canvas.
`content_pack_catalog_plan` is the separate narrow persistence path for the
strict authoring contract itself: it diffs only
`devkit/content_forge/packs.json`. `content_pack_catalog_apply` defaults to a
SHA rehearsal and needs `SAVE CONTENT PACK` for a real save; it does not apply
module source.
`content_pack_apply` is deliberately one named source or direct legacy-record
target at a time, dry-run by default, and never writes generated IDs, exports,
or normal build layers. Follow a non-dry apply with `content_pack_verify`, then
the ordinary reviewed build. See [`../content_forge/README.md`](../content_forge/README.md).

## Optional local Module Studio

The MCP/JSON surfaces remain first. If a human wants a CBO-style visual way to
sort results and stage semantic edits, launch the optional loopback-only Studio
with `./devkit/SoDDev.bat studio`. It reuses these exact tools; it adds no MCP
write capability, no generic file editor, and no build/export action. Its
editor always plans a diff first, carries that plan's SHA into a dry-run, and
requires an explicit `APPLY SOURCE` confirmation before a source-only apply.
See [`../module_studio/README.md`](../module_studio/README.md).

## Install the local runtime

The project-local runtime is intentionally isolated in `devkit/.venv`:

```powershell
py -3 -m venv devkit\.venv
.\devkit\.venv\Scripts\python.exe -m pip install -r devkit\mcp_server\requirements.txt
```

## Test it

```powershell
.\devkit\.venv\Scripts\python.exe devkit\mcp_server\test_server.py
```

The test makes both an in-memory MCP call and a real STDIO MCP call. That
second check is important: stdout is the protocol stream and must never contain
ordinary logging or status output.

## Connect a local Codex client

OpenAI documents that local Codex clients support STDIO MCP servers and share
MCP configuration. Use absolute paths because the host launches servers from
its own working directory:

```powershell
codex mcp add sod-modern-devkit -- "D:\absolute\path\to\sod_modern\devkit\.venv\Scripts\python.exe" "D:\absolute\path\to\sod_modern\devkit\mcp_server\server.py"
```

Then start a new local Codex session (or refresh the local client) and inspect
the configured server with `codex mcp list` or `/mcp`. A configuration change
cannot add a tool to an already-running hosted session.

The official references used for this design are:

- [OpenAI: Model Context Protocol for Codex](https://learn.chatgpt.com/docs/extend/mcp)
- [MCP Python SDK v2](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Python SDK: connecting a STDIO server](https://py.sdk.modelcontextprotocol.io/get-started/real-host/)
