# Campaign State Doctor

The Campaign State Doctor is the DevKit layer for bugs the M&B 1.011 compiler
accepts but the campaign can still execute incorrectly: competing AI intent,
stale party/slot state, and time-driven writers that undo each other.

It is deliberately LLM-first and read-only. Its canonical inputs are
`src/scripts/` and `src/triggers/`; it never imports module data, starts the
game, runs a builder, or writes `compile/` / `_export/`.

## What it models

- Durable party AI fields, party/faction/troop slots, key party lifecycle
  writes, and global-variable reads/writes.
- Exact source operation order inside every modeled script or simple trigger.
- A bounded static call graph from simple-trigger roots, preserving the known
  hourly/daily cadence and direct call path.
- M&B `try_begin` / `else_try` / `try_end` branch boundaries. It proves only
  explicit mutual exclusion; uncertain paths remain warnings rather than being
  silently dismissed.
- Narrow temporal proofs for a completed local fallback guard (for example,
  `:deployed = 1` before a later `:deployed == 0` branch) and the engine's
  direct `spawn_around_party` → `reg0` party rebinding. These are recognized
  only when the exact local branch and source order prove them.
- An adjacent `spai_undefined` → intended-state reset/reapply remains a
  source-mapped `info` finding rather than a warning, since it deliberately
  forces `script_party_set_ai_state` to rerun its initialization path.
- Checked-in state contracts under `contracts.json`. A contract can convert a
  known gameplay rule into a permanent regression detector with source-mapped
  counterexample evidence.
- Generic opt-in `party_ai_intent` contracts for stationary behavior, literal
  patrol-radius ranges, escort attachment/detachment, guarded raid returns,
  and guarded despawns. A contract names its own `scope_scripts`; the doctor
  never claims a generic helper belongs to a party template from its name.

The first contract formalizes the Black Khergit invariant that a pitched camp
must keep hold AI until it deliberately relocates or is still approaching a
target. It would have identified the prior daytime travel overwrite before an
in-game check.

## AI intent contracts

The legacy `stationary_camp` contract remains supported. New behavior rules
use `kind: "party_ai_intent"` plus one of `stationary`, `patrol`, `escort`,
`raid_return`, or `despawn`. Keep a rule narrow and source-reviewable:

```json
{
  "id": "example-patrol",
  "kind": "party_ai_intent",
  "intent": "patrol",
  "party_template": "pt_example_patrol",
  "scope_scripts": ["script_example_refresh_patrol"],
  "expected_behavior": "ai_bhvr_patrol_location",
  "minimum_radius": 4,
  "maximum_radius": 12
}
```

`escort` accepts `attach_to` and optional `require_detach`; `raid_return`
accepts `return_behavior`, `return_target`, and `return_when`; `despawn`
accepts `despawn_when`. Dynamic radius/selector values and unresolved engine
behavior remain unproven rather than assumed safe. Add `party_selector` when
one scoped helper manipulates several local party variables; this prevents a
behavior write for one party from being paired with a radius/target write for
another.

## Boundaries

This is not a game emulator. It cannot prove save contents, random outcomes,
engine AI resolution, or dynamic party identity hidden behind locals. Exact
symbolic selectors are intentionally kept separate unless a contract supplies
stronger role/state evidence. Recursive call paths and paths beyond depth 12
are reported as unresolved boundaries, never flattened into invented runtime
order.

## CLI

Run from the module root:

```powershell
py -3 -B devkit\campaign_state_doctor\campaign_state_doctor.py summary --format markdown
py -3 -B devkit\campaign_state_doctor\campaign_state_doctor.py findings --severity warning --limit 20
py -3 -B devkit\campaign_state_doctor\campaign_state_doctor.py contracts --contract-id black_khergit_camped_ai_stationary
py -3 -B devkit\campaign_state_doctor\campaign_state_doctor.py ai-intents
py -3 -B devkit\campaign_state_doctor\campaign_state_doctor.py resource slot_party_black_khergit_origin
py -3 -B devkit\campaign_state_doctor\campaign_state_doctor.py timeline party_ai_behavior::camp_party:behavior
```

The convenience front door routes the same JSON CLI through
`./devkit/SoDDev.bat state summary`.

The normal workflow is:

1. Start with `summary` to establish coverage, contract status, and bounded
   findings.
2. Use `findings` to select an error or possible overwrite.
3. Use `resource` to list every source-mapped reader and writer.
4. Use `timeline` to inspect the exact operation/branch evidence and every
   trigger route that reaches it.
5. Add a narrow contract only after a gameplay invariant is understood and
   reviewed; do not use contracts to hide a warning.

## MCP

The DevKit MCP server exposes the same deterministic model:

- `campaign_state_summary`
- `campaign_state_findings`
- `campaign_state_resource`
- `campaign_state_timeline`
- `campaign_state_contracts`
- `campaign_ai_intents`

Use the MCP result data rather than scraping CLI text. The CLI is the
offline, deterministic fallback.

## Verify

```powershell
py -3 -B devkit\campaign_state_doctor\test_campaign_state_doctor.py
```
