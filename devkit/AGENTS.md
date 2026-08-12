# DevKit: LLM-First Rules

`devkit/` exists for Codex/LLM use first. Human-facing UI is optional and must
never be the only way to discover, inspect, diagnose, or automate a system.

## Interface order

1. Typed MCP tool with structured output.
2. Deterministic CLI with a JSON mode.
3. Checked-in machine-readable catalog/schema.
4. Text report, DOT artifact, or UI only as a convenience layer.

## Non-negotiable tool behavior

- Default to read-only operations. Mutation must use a separate, explicitly
  named apply tool with a dry-run/diff path, a current-content hash guard, and
  source-only scope.
- Every diagnosis must return source provenance: source fragment, generated
  module, export layer, or explicit absence of that evidence.
- Bound result sizes and expose filters so an agent can inspect a large module
  without flooding its context window.
- Use stable IDs and JSON-safe values. Do not make an LLM scrape prose to use a
  result that could be structured.
- Update `manifest.json`, the result-envelope contract, and automated tests
  whenever an agent-callable capability is added or changed.
- An MCP stdio server must never print to stdout; stdout is reserved for MCP
  protocol messages. Use standard logging (stderr) for diagnostics.

## Workflow

An agent approaching an unfamiliar workspace should start with
`workspace_audit`; otherwise start with `devkit_catalog` or `devkit_health`,
then call the narrowest tool that can prove a claim. For text in the wrong
dialogue, menu, overlay, or message location, run `string_integrity` before
`text_explain`; use `text_export_parity` when generated/export drift or
quick-string reindexing is plausible, `register_history` for cross-screen state,
and `string_trace` for raw layer lookup before proposing a source edit. For dialogue flow, inspect compiled
order before changing a fragment because M&B 1.011 selects the first matching
NPC dialogue line. Then use `code_find`, `linked_context`, and
`change_impact`; create a `patch_plan` before any explicit
`apply_source_edits` call, then run `verify_change`. Never use the router to
write `compile/` or `_export/`; those remain reviewed build outputs.

For authored dialogue, prefer `dialogue_find` then `dialogue_context` and
`dialogue_patch`; for a new route, use `dialogue_create_plan` with its anchored
JSON contract rather than free-form source. Apply creation only through
`dialogue_create_apply` with both the source SHA and exact plan ID; use
`dialogue_verify` after resolving the new stable route ID. It exposes source
order and static fallback shadows so an LLM does not mistake a later NPC route
for a reachable route. For
presentation code, prefer `presentation_find`, `presentation_canvas`, and
`presentation_patch`; inspect shared position-register consumers before
`presentation_apply`, then use `presentation_verify`. `presentation_preview`
may write a diagnostic SVG only under `devkit/output/`; it is never a source
or export path. All semantic applies delegate to the same Change Router source
gate and retain the dry-run/hash/source-only guarantees.

For an unfamiliar non-dialogue/non-presentation module area, begin with
`module_atlas_summary`, then run `module_integrity` before concluding a direct
reference is broken. Use `module_find` to get a stable entity ID and
`module_context`/`module_graph` to prove source ownership, generated
provenance, operations, direct links, and available actions. Prefer
`menu_flow`, `script_flow`, `mission_timeline`, `trigger_timeline`,
`quest_registry`, and `entity_references` over broad search when the question
matches one of those models. `module_patch`/`module_apply` are the semantic
authoring path for constants, menus, missions, quests, scripts, and simple
triggers. They share the router gate; do not use them to edit dialogue or
presentation semantics, which require their specialist composers. A
top-level removal with direct inbound Atlas references requires explicit
`allow_referenced_removal` acknowledgement after those references have been
reviewed and migrated deliberately.

For content that crosses dialogue, quest/event flow, campaign AI, troop/item
records, or presentation layout, begin with `content_forge_summary` and
`content_pack_explain`. A Content Pack must carry its brief, lore constraints,
tone, acceptance criteria, typed slices, and declared verification evidence;
do not flatten that context into raw source. Use `content_pack_validate`, then
`content_pack_plan` and `content_pack_review` before any apply. The review
canvas is a human convenience, not authority: MCP/CLI JSON and the specialist
plans remain canonical. `content_pack_apply` applies exactly one named change
with the current content-plan ID and SHA, dry-run by default. Source changes
delegate to Feature Authoring; troop/item records delegate to Balance Lab and
retain its legacy acknowledgements. New troop/item records and reordering are
intentionally outside this pack compiler because ID-sensitive legacy order
must be reviewed explicitly. Follow a non-dry change with
`content_pack_verify`; it rechecks first-match/source/order evidence, current
AI intent contracts, and optional deterministic scenarios before the normal
reviewed build.

To persist a strict Content Pack itself, use `content_pack_catalog_plan` then
`content_pack_catalog_apply` rather than editing `packs.json` directly. This
is a separate contract-only SHA gate: its real save requires the exact
catalog-plan ID, current catalog SHA, and `SAVE CONTENT PACK` confirmation;
it writes only `devkit/content_forge/packs.json` and never applies content,
module source, generated IDs, or exports. Module Studio's Content Forge page
is a human-facing renderer/editor for this same contract, not an alternate
authoring authority.

For any change where top-to-bottom order could affect assembly, first-match
dialogue, positional IDs, or an engine callback, begin with `order_summary`
and `order_explain`. Use `order_risk` before proposing a move and
`order_plan_move` to obtain the exact anchored diff and its current SHA. The
only automatic move paths are a pair of entries in the same explicit
`src/**/_order*.txt` manifest or a pair of dialogue routes in the same source
fragment; `order_apply_move` is dry-run by default. It must never be used to
rename folders, sort files wholesale, hand-edit `compile/ids`, or write a
generated/export layer. After a reviewed normal build, use `order_diff` and
`order_verify`; any generated-ID movement requires a deliberate compatibility
decision and targeted in-game smoke path.

For troop/item balance work, start with `balance_summary`, then use
`balance_item`/`balance_troop` to establish exact evaluated stats, inventory
pool, source ownership, and generated-ID parity. Use `balance_compare`,
`balance_upgrade_tree`, and `balance_outliers` before treating a numeric
outlier as a required gameplay change. `compile/module_items.py` and
`compile/module_troops.py` are confirmed legacy authoring inputs in this
workspace—not exports—but their record order is still ID-sensitive. The
Balance Lab may only plan record-local semantic changes; it never moves or
adds records, writes `compile/ids` or `_export`, or bypasses a normal reviewed
build. Review its unified diff, current source SHA, and plan SHA first;
`balance_apply` is dry-run by default and a non-dry write requires an explicit
legacy-authoring acknowledgement (plus a protected-record acknowledgement for
hardwired records). Derived upgrade variants are view-only.
Before comparing different rosters, use `balance_campaign_cohorts` to verify
that they coexist in the same campaign. The five SoD player cultures are
mutually exclusive new-game choices, while native kingdoms are persistent
world realms. Use `balance_imperial_invasion` for Imperial work; it reports
the endgame force's core waves and campaign pressure/supply/counterplay
contracts instead of flattening it into a normal faction average.
Use `balance_player_start_factions` before changing a selected-culture
reinforcement template or binding. It models the actual center and lord
template selection weights and keeps the five alternatives separate.
Use `balance_player_start_progression` before changing a direct player-culture
upgrade, and `balance_faith_ascensions` before changing a Noble candidate or
Faith troop. Their static contracts protect rank progression while preserving
theme-specific equipment and role trades.
Use `balance_native_kingdoms` before changing a Native A/B/C template or
Native upgrade route. It treats the five kingdoms as coexisting campaign
peers, but preserves their doctrine instead of demanding one generic roster.
Use `balance_mercenary_guilds` before changing mercenary demand, guild role
fit, contract selection, AI company formation, or mercenary contract dialogue.
It treats guilds as asymmetric service specialists and verifies that a
job-shaped AI roster keeps its original company size; player hiring remains a
separate, player-chosen composition.

Use the CBO-inspired M&B Workbench when a task crosses discovery, validation,
tests, contracts, and release evidence. Start with `workbench_impact`, choose
an exact returned Atlas entity, and run `workbench_scope_check` at a fixed
`fast`, `standard`, or `deep` depth. The Workbench is not a generic command
runner: scenarios are checked-in fixed builtins/tests, and its contracts are
declarative static expectations. `workbench_coverage` labels only exact
contract/scenario/test/generated evidence; broad context is never proof.
Finish meaningful changes with `workbench_release_readiness` and an explicit
in-game smoke path. `workbench_draft` creates a disabled DevKit-only planning
packet; it never activates content. Baselines/reports/drafts are confined to
ignored Workbench artifact folders and never replace the SHA-guarded semantic
source apply gate.

For a release candidate after the ordinary reviewed build, run `release_gate`.
It is a fixed read-only all-layer preflight: staged source/generated/all-export
parity, clean staged compiler diagnostics, the exact intentional-blank string
baseline, zero dialogue-model errors, and clean order/ID contracts must all
pass. Do not broaden its approval contract to silence a new warning; inspect
the source path and exact count first, then make a deliberate reviewed update
only when the behavior is genuinely intentional.

`module_studio` is an optional local human convenience surface, not a second
toolchain. It is intentionally loopback-only and mirrors the existing Atlas,
Dialogue Composer, Presentation Layout, and Workbench operations. Use MCP/CLI
results for automation first. In Studio, inspect an exact entity/route/overlay
and its static links before generating a semantic plan; review its diff and
base SHA, rehearse the dry-run, and use a non-dry source apply only with the
explicit confirmation. Studio must never grow a generic file editor, arbitrary
command runner, build button, or export writer.
