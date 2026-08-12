# SoD Modern DevKit

`devkit/` is the home for standalone authoring and diagnostic tools. It is
LLM/Codex-first by design: typed MCP tools and deterministic JSON output are
the primary interfaces; a human UI is only an optional convenience layer. It
is deliberately separate from both `build/` and `compile/`: a DevKit tool must
not be imported by the module-system compiler or change a live export as part
of normal use.

Each focused capability lives in its own subfolder with its own usage notes and
tests.  Generated diagnostic artifacts belong in `devkit/output/`, which is
ignored by Git.

## Current slices

| Slice | Purpose |
| --- | --- |
| `dialogue_inspector/` | Trace compiled dialogue order and source provenance, inspect string/register use, search all string layers, and export a dialogue-state graph. |
| `workspace_audit/` | Establish the modular source, generated compile, legacy processing, export, ordering, freshness, and validation topology before diagnosis. |
| `string_integrity/` | Preflight visible text sinks and s-register flow, including dynamic selector boundaries and source provenance. |
| `text_export_parity/` | Replay the legacy processor chain in temporary staging and prove or pinpoint generated/source-to-export text-table drift without changing live exports. |
| `release_gate/` | Run one strict read-only release preflight that requires full source/generated/all-export parity, clean staged compiler diagnostics, exact approved intentional blank text sinks, zero dialogue-model errors, and intact order/ID contracts. |
| `module_blueprint/` | Give a coherent feature a stable checked-in identity and prove its exact source, symbols, order, slot ownership, AI intent contracts, downstream impact, and focused test declarations before a legacy source edit. |
| `feature_authoring/` | Compile an LLM-first typed Feature Intent through real engine entrypoints and the existing Blueprint/Atlas/dialogue/presentation specialists; produce reviewed per-source SHA plans, bounded traces, semantic baselines, and focused verification without raw tuple authoring. |
| `text_execution_ledger/` | Explain why a text sink can render through conditions, writers, selectors, scripts, globals, transitions, and source provenance. |
| `string_provenance/` | Follow `s`-register writers through literal generated `call_script` paths and enclosing branches, separating actual writer paths from unresolved clobber boundaries. |
| `dialogue_model_checker/` | Prove branch-free dialogue contradictions, first-match shadows, overlaps, ambiguous player choices, and terminal dead states while preserving complex condition blocks as boundaries. |
| `campaign_state_doctor/` | Model durable campaign state and checked-in AI intent contracts for stationary camps, patrols, escorts, raid returns, and despawns. |
| `slot_lifecycle_lint/` | Enforce reviewed durable-slot ownership, approved handoffs, reset lifecycles, and multi-system sharing review candidates. |
| `campaign_scenario_fuzzer/` | Generate deterministic valid campaign states and execute a deliberately safe literal script subset to return reproducible counterexamples or inconclusive boundaries. |
| `semantic_change_diff/` | Capture/diff dialogue precedence, state writers, text sinks, generated IDs, trigger effects, and export hashes across an edit. |
| `change_router/` | Find code, traverse its modular/generated/runtime links, assess impact, plan exact edits, apply only SHA-guarded source patches, and verify safely. |
| `dialogue_composer/` | Semantically find, inspect, reorder, edit, and deterministically create dialogue routes from an anchored JSON contract while surfacing first-match hazards and delegating every apply to Change Router. |
| `presentation_layout/` | Reconstruct static presentation overlay layouts, diagnose bounds/overlap/binding risks, produce SVG diagnostics, and semantically edit direct layout operations through Change Router. |
| `module_atlas/` | Index every modular source area as a graph of constants, routes, menus/options, missions/triggers, presentations, quests, scripts, and simple triggers; detect structural reference risks and perform guarded semantic authoring outside dialogue/presentation specialists. |
| `order_control/` | Make source manifests, authored route/record order, generated-ID shifts, and engine callback prefixes explicit; assess anchored move risk, plan guarded manifest/dialogue moves, and diff order baselines without touching generated/export layers. |
| `troop_item_balance/` | Evaluate legacy M&B 1.011 item/troop authoring, trace equipment and progression, map real campaign cohorts, player-start and coexisting-Native reinforcement pressure, mercenary contract niches, tier trajectories, and Imperial invasion waves, surface review candidates, and plan narrow SHA-guarded balance edits without touching generated IDs, order, or exports. |
| `workbench/` | CBO-inspired, M&B-native fixed workflows for impact packets, scoped validation, declarative contracts, coverage maturity, registered scenarios, release evidence, and disabled authoring drafts. |
| `module_studio/` | Optional loopback-only CBO-style viewer/editor for Atlas, dialogue, presentation, text, and Workbench evidence. Its Presentation Workshop adds visual overlay selection, local drag staging, layout/content controls, creation, and the same semantic diff/SHA/dry-run gates. |
| `mcp_server/` | Present the DevKit’s diagnostics and explicitly named guarded source editing as typed local MCP tools for Codex and other LLM hosts. |

## Agent contract

Start with [`manifest.json`](manifest.json) to discover capabilities, and use
the shared [`tool-result.v1`](contracts/tool-result.v1.schema.json) result
envelope for MCP responses. Local agent rules live in [`AGENTS.md`](AGENTS.md).
The MCP server setup and test instructions are in
[`mcp_server/README.md`](mcp_server/README.md).

This is intentionally a small foundation.  Future slices can sit alongside it
without becoming implicit build dependencies.

For Windows shell use, [`SoDDev.bat`](SoDDev.bat) is a convenience front door;
MCP and the JSON CLI remain the primary interfaces. It routes `state`,
`slots`, `dialogue-model`, `provenance`, `fuzz`, `semantic`, `gate`, `blueprint`, and `feature` to their
matching deterministic slices. For example:
`./devkit/SoDDev.bat dialogue-model summary`.

For a feature-level source impact plan before editing an ordered legacy slice,
use `./devkit/SoDDev.bat blueprint compile campaign-dispatch`. It validates the
checked-in Blueprint contract but deliberately has no apply mode; source edits
still use the existing specialist or Change Router SHA guard.

For an LLM-first feature workflow that hides the engine/order complexity, use
`./devkit/SoDDev.bat feature explain --feature-id campaign-dispatch`, then
`feature plan`. The Feature Authoring Compiler resolves real engine
entrypoints, accepts only typed JSON operations (never raw Python tuples), and
applies one reviewed SHA-guarded source target at a time. See
[`feature_authoring/README.md`](feature_authoring/README.md).

For a release candidate, use `./devkit/SoDDev.bat gate run` for the isolated
strict preflight, or `cmd /c build_module.bat --release-gate --no-cache` to
run it after the normal canonical build.

For a local visual sorting/authoring surface, run
`./devkit/SoDDev.bat studio` and open the printed `127.0.0.1` URL manually.
The Studio never opens a browser, builds the module, or writes exports; see
[`module_studio/README.md`](module_studio/README.md) for its endpoint and
semantic-edit contract.
