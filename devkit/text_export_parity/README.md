# Text Export Parity

This DevKit slice answers a question that record counts cannot: does the
current legacy processor chain generate the same text-bearing files that the
game is loading from `_export/`?

It copies the processor inputs into a system temporary workspace, redirects
that copy's `module_info.export_dir`, replays the fixed processor sequence, and
compares the staged output against the live export. It never runs the live
build and never writes real `compile/` or `_export/` paths.

Default `text` scope covers `strings.txt`, `quick_strings.txt`, dialogue text
and states, plus menus, presentations, scripts, triggers, mission templates,
quests, and simple triggers that can carry inline text or quick-string
references. `--scope all` adds every processor-derived export.

`--source-build` also assembles modular source in the same staging workspace:

`src/**` -> staged `compile/module_*.py` -> staged legacy exports -> live `_export/*.txt`

## CLI

```powershell
py -3 devkit\text_export_parity\text_export_parity.py summary
py -3 devkit\text_export_parity\text_export_parity.py summary --source-build
py -3 devkit\text_export_parity\text_export_parity.py summary --scope all --max-diffs 10
py -3 devkit\text_export_parity\text_export_parity.py summary --source-build --format markdown
```

JSON is the primary output. It includes bounded first-difference evidence,
source/generated provenance per export, source freshness, staged generated
module drift, and a fingerprinted assertion that protected live compile/export
surfaces were unchanged. Each staged builder/processor result also carries
bounded `WARNING:`/`ERROR:` diagnostic counts, so a release gate can reject a
non-fatal compiler warning without scraping a clipped console transcript. When
`quick_strings.txt` differs, it also reports
bounded live-only and staged-only records, separating stale table entries from
an order-only difference that would otherwise make menu IDs hard to diagnose.

`process_global_variables_unused.py` is intentionally excluded: it produces a
documentation report, not a module export. Every processor that changes an
export is still run in the checked-in order.

## States

- `generated_to_export_parity` — current generated modules replay to the same
  live text exports.
- `generated_to_export_parity_source_stale` — generated/export data agree, but
  some modular source is newer; rerun with `--source-build`.
- `source_to_export_parity` — the staged full source/build/export route agrees
  with the live export.
- `mismatch` — staged output and live data differ. Review the exact evidence
  before any reviewed build replaces a live export.

Parity does not simulate engine execution. Use `string_integrity`,
`text_explain`, and `register_history` to trace dynamic s-register behavior.

## Verify

```powershell
py -3 -B devkit\text_export_parity\test_text_export_parity.py
```
