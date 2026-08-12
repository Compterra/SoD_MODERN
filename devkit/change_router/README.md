# Change Router

The Change Router turns a search result into a bounded, source-owned change
workflow for the Mount & Blade 1.011 module system:

`find → linked context → impact → patch plan → guarded source edit → verify`

It is LLM-first. MCP and deterministic JSON are the primary interfaces; no
human dashboard is required to use it effectively.

## What it links

For a modular source fragment, the router returns:

- stable source target IDs, exact source excerpts, hashes, and syntax state;
- section ordering and neighboring fragments;
- generated `module_*.py` source-marker ranges;
- expected export layers, including both `strings.txt` and
  `quick_strings.txt` where applicable;
- script callers/callees, globals, registers, menu transitions, and visible
  text sinks from the Text Execution Ledger;
- related source fragments sharing meaningful symbols;
- likely narrow static tests; and
- a source-only unified diff plus expected generated/export consequences.

The index is persisted under `devkit/.cache/` and ignored by Git. It is
rebuilt incrementally from source, generated-module, and order-manifest
timestamps.

## MCP workflow

1. `code_find(query="past_life")` returns a source target ID and line.
2. `linked_context(target_id=..., focus_line=...)` gives ownership, generated
   mapping, order, execution links, and test candidates.
3. `change_impact(target_id=...)` establishes downstream risk before editing.
4. `patch_plan(target_id=..., edits=[...])` produces a deterministic diff and
   the required source SHA-256.
5. `apply_source_edits(..., expected_sha256=..., dry_run=true)` is the default
   rehearsal. Set `dry_run=false` only after reviewing that exact diff.
6. `verify_change(...)` checks syntax, ordering, generated freshness, selected
   static tests, and optionally an isolated staging build.

`apply_source_edits` can write only an existing `src/**/*.py` target returned
by `code_find`. It requires the current SHA-256, writes atomically, and never
writes `compile/` or `_export/`. A reviewed normal project build remains a
separate explicit action.

## Edit shape

The router is mechanical by design. An LLM first finds and reads the exact
fragment; it then gives the router unambiguous anchors:

~~~json
[
  {
    "old_text": "old exact text",
    "new_text": "new exact text",
    "occurrence": 1,
    "expected_occurrences": 1
  }
]
~~~

`expected_occurrences` defaults to `1`. This prevents a broadly repeated
substring from silently changing the wrong place.

## CLI

Run from the module root:

~~~powershell
py -3 devkit\change_router\change_router.py summary
py -3 devkit\change_router\change_router.py find "past_life" --scope source
py -3 devkit\change_router\change_router.py context "source:src/menus/0000_hardcoded_mb1011/past_life_explanation.py" --focus-line 20
py -3 devkit\change_router\change_router.py impact "source:src/menus/0000_hardcoded_mb1011/past_life_explanation.py"
py -3 devkit\change_router\change_router.py plan "source:src/menus/0000_hardcoded_mb1011/past_life_explanation.py" --edits '[{"old_text":"old","new_text":"new"}]'
py -3 devkit\change_router\change_router.py verify "source:src/menus/0000_hardcoded_mb1011/past_life_explanation.py" --run-tests --stage-build
~~~

`apply` is dry-run unless `--apply` is explicitly supplied together with the
SHA returned by `plan`. On Windows shells where inline JSON quoting is awkward,
`plan` and `apply` also accept `--edits-file path\to\edits.json`; the
file must remain inside the workspace.

## Limits

The router models static source and generated evidence. It does not claim that
every branch, dynamic selector, or game-state value is reachable. When source
is newer than its generated output, it reports that boundary instead of
pretending that stale compiled evidence is current.

## Verify

~~~powershell
py -3 -B devkit\change_router\test_change_router.py
~~~
