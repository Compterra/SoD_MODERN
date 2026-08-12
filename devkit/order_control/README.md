# Order Control Plane

`order_control/` makes Mount & Blade 1.011 ordering visible and reviewable as
first-class data. It is an LLM/Codex-first slice: MCP and deterministic JSON
are the supported interfaces; any human-facing presentation is only a thin
adapter over the same functions.

Order is executable behavior in this module system. A source manifest affects
assembly order; dialogue routes are first-match; generated record order creates
numeric IDs; and the engine calls specific hardcoded scripts by position. A
normal text search can find an identifier, but it cannot prove which earlier
record can shadow it or what a fragment move could shift downstream.

## What it covers

- Explicit `src/**/_order*.txt` fragment manifests and their declared policy.
- Authored record order, including child records and same-fragment dialogue
  route order.
- Source-to-generated provenance markers and compiled dialogue mapping.
- Generated `compile/ids/ID_*.py` tables as read-only compatibility evidence.
- Checked-in protected contracts for strict manifests, the legacy hardcoded
  menu-ID block, and `game_*` callback-script IDs.
- Baseline/diff reports that compare fragment order and generated ID tables.

It does not sort folders, rename section folders, hand-edit `compile/ids`,
write generated modules or `_export`, execute engine callbacks, or certify save
compatibility. Those boundaries are deliberate.

## Agent workflow

1. Call `order_summary`, then `order_explain` for an exact `source:`,
   `module:`, `dialogue:`, or generated-ID target.
2. Call `order_risk` with a target, anchor, and `before`/`after` position.
3. Review `order_plan_move`'s unified diff and `base_sha256`.
4. Rehearse `order_apply_move` with `dry_run=true`; only use a non-dry apply
   after an explicit reviewed decision.
5. Run the normal reviewed build, inspect generated module/ID/export diffs,
   then call `order_verify` and perform the target in-game smoke path.

Only two automatic move classes exist:

- two source fragments under the same declared `_order*.txt` manifest; and
- two dialogue routes in the same source fragment.

Fragment moves change a single manifest line only. Dialogue moves delegate to
the existing Dialogue Composer and Change Router SHA gate. Generic entity,
folder, and generated-ID reordering intentionally have no automatic write path.

## JSON CLI

Run from the workspace root:

```powershell
py -3 -B devkit\order_control\order_control.py summary
py -3 -B devkit\order_control\order_control.py map --area menus --domain source-fragments --query past_life
py -3 -B devkit\order_control\order_control.py explain source:src/menus/0000_hardcoded_mb1011/past_life_explanation.py
py -3 -B devkit\order_control\order_control.py contracts
```

Plan and rehearse an order move:

```powershell
py -3 -B devkit\order_control\order_control.py plan-move `
  source:src/menus/0000_hardcoded_mb1011/tutorial.py `
  source:src/menus/0000_hardcoded_mb1011/start_game_1.py `
  --position before

py -3 -B devkit\order_control\order_control.py apply-move `
  source:src/menus/0000_hardcoded_mb1011/tutorial.py `
  source:src/menus/0000_hardcoded_mb1011/start_game_1.py `
  --position before --expected-sha256 <sha-from-plan>
```

`apply-move` is a dry run unless `--apply` is supplied. A baseline/report can
write only under ignored `devkit/order_control/baselines/` or
`devkit/order_control/reports/`:

```powershell
py -3 -B devkit\order_control\order_control.py baseline --label before-menu-work
py -3 -B devkit\order_control\order_control.py diff --baseline before-menu-work
py -3 -B devkit\order_control\order_control.py verify --baseline before-menu-work
```

The CBO-style convenience front door also routes `SoDDev.bat order ...` to this
CLI. See the DevKit MCP server for the equivalent typed `order_*` tools.

## Contracts

[`contracts/manifest.json`](contracts/manifest.json) is intentionally small
and reviewed. It records only invariants that are already meaningful to this
module system:

- strict generated manifests must be complete and duplicate-free;
- the hardcoded M&B 1.011 / old SoD menu slice retains its declared generated
  IDs (including the intentional legacy gap); and
- hardcoded `game_*` callbacks retain their generated script sequence.

Add a contract only when it captures a concrete engine, compatibility, or
deliberately frozen legacy boundary. A baseline observes current state; it does
not redefine an invariant.

A non-dry move inside an active protected engine/legacy contract is refused
unless the caller explicitly supplies `allow_protected_contract_change=true`
(CLI: `--allow-protected-contract-change`). That override records intent; it
does not waive the required normal build diff, contract review, compatibility
decision, or in-game smoke path.

## Tests

```powershell
py -3 -B devkit\order_control\test_order_control.py
```

The fixture test proves strict-manifest and protected-ID checks, baseline
drift, manifest move planning/dry-run/apply, and same-fragment dialogue move
planning. It never changes the live module tree.
