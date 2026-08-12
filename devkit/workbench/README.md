# SoD Modern Workbench

The Workbench brings the useful operating model of the CBO DevKit to this
Mount & Blade 1.011 module system without pretending both games have the same
data model or runtime. It is an LLM-first coordination layer built on the
existing Module Atlas, Change Router, dialogue/presentation specialists,
string tools, and workspace audit.

It does not build a dashboard first and it does not offer arbitrary command
execution. Every result is deterministic JSON; every executable validation
step is named in a checked-in scenario or fixed by the selected validation
depth.

## Workbench model

| CBO pattern | M&B-native implementation |
| --- | --- |
| `impact` packet | `workbench_impact`: semantic owner, source/generated/export effects, order, links, coverage, and a fixed next plan. |
| `scope-check` | `workbench_scope_check`: fast source parse/order/freshness; standard adds selected tests; deep adds an isolated area build. |
| Contracts | `contracts/manifest.json`: declarative source topology, direct-reference integrity, text observability, and DevKit safety expectations. |
| Scenarios | `scenarios/manifest.json`: registered structural sentinels and fixture checks; no caller-supplied shell commands. |
| Coverage | `workbench_coverage`: exact contract/scenario targets, generated provenance, and static test candidates without claiming broad context is proof. |
| Order report | `workbench_order_report`: protected manifest/ID/callback contracts, generated-marker parity, dialogue-order hazards, and optional baseline drift. |
| Release readiness | `workbench_release_readiness`: static/manual checklist with explicit in-game gates, never a false release certificate. |
| Disabled drafts | `workbench_draft`: DevKit-only authoring packets that cannot activate source content. |

## Recommended agent workflow

1. Run `workbench_doctor` once when setting up or resuming a workspace.
2. Use `workbench_impact` on an exact Atlas ID, source target, identifier, or
   phrase. Set `include_text_evidence=true` for a wrong-string investigation.
3. Choose an exact entity, then run `workbench_scope_check` at `fast` before a
   plan; use `standard` before a meaningful change and `deep` when an isolated
   area build is warranted.
4. Use `dialogue_patch`, `presentation_patch`, or `module_patch` for the
   actual semantic source plan. Review its diff and SHA before the dry-run
   apply; the Workbench never bypasses that gate.
5. Use `workbench_contract_drift`, `workbench_coverage`, and a registered
   scenario to show what evidence exists and what remains unproven.
6. When top-to-bottom ordering is in scope, use `order_explain`/
   `order_risk` before a move and `workbench_order_report` after a normal
   reviewed build. Treat any generated-ID shift as an explicit compatibility
   decision rather than an incidental side effect.
7. Finish with `workbench_release_readiness`, the normal reviewed build, and a
   targeted in-game smoke path. Check both `strings.txt` and
   `quick_strings.txt` when visible text is involved.

## CLI

For a CBO-style Windows-safe front door, use `devkit\SoDDev.bat`; it invokes
the same Workbench CLI through a process-local PowerShell execution-policy
bypass and does not alter machine policy. `SoDDev.ps1` is available directly
in already policy-enabled sessions.

```powershell
.\devkit\SoDDev.bat doctor
.\devkit\SoDDev.bat impact past_life_explanation
.\devkit\SoDDev.bat scope-check <module-entity-id> --depth standard

# Direct deterministic JSON CLI (the same command surface)
py -3 -B devkit\workbench\workbench.py doctor
py -3 -B devkit\workbench\workbench.py impact past_life_explanation
py -3 -B devkit\workbench\workbench.py impact "wrong text" --include-text-evidence
py -3 -B devkit\workbench\workbench.py scope-check <module-entity-id> --depth standard
py -3 -B devkit\workbench\workbench.py order-report --baseline before-order-work
py -3 -B devkit\workbench\workbench.py contract-drift
py -3 -B devkit\workbench\workbench.py coverage --area menus --gaps-only
py -3 -B devkit\workbench\workbench.py scenario-list
py -3 -B devkit\workbench\workbench.py scenario-run atlas-structure-sentinel
py -3 -B devkit\workbench\workbench.py release-readiness
py -3 -B devkit\workbench\workbench.py draft menu "Quartermaster Branch"
```

`contract-baseline`, `draft`, and `--write-report` perform intentional,
confined artifact writes only:

- baselines: `devkit/workbench/contracts/baselines/`
- drafts: `devkit/workbench/drafts/`
- reports: `devkit/workbench/reports/`

All are ignored local artifacts. They never touch `src/`, `compile/`, or
`_export/`, and a draft is not active module content.

## Evidence levels

- **source-only**: an authored record is known, but no exact additional
  evidence is associated with it.
- **generated provenance**: the generated module maps back to the source
  fragment.
- **test candidate**: Change Router selected a narrow static test candidate.
- **registered scenario**: a named fixed scenario explicitly targets it.
- **static contract**: a declarative current contract explicitly targets it.

These are intentionally conservative. Static analysis does not run M&B menu
conditions, evaluate dynamic selectors, or show a game screen. A passing
contract or scenario still needs normal build review and targeted in-game
proof where engine behavior matters.

## Test

```powershell
py -3 -B devkit\workbench\test_workbench.py
```

The fixture creates an isolated eight-area module workspace and proves impact,
fixed scope checking, contract drift/baselining, coverage, registered scenario
execution, text lint, and disabled draft behavior.
