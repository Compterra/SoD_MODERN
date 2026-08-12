# String Integrity Checker

This DevKit slice performs a read-only semantic preflight over generated
Mount & Blade 1.011 modules. It turns the question “why did that UI or
dialogue show the wrong text?” into bounded evidence:

- visible text sinks in dialogues, menus, presentations, messages, and
  overlays;
- each `{sN}` substitution used by that sink;
- the last lexical string writer that can be proven, including known
  `call_script` effects;
- generated-line and source-fragment provenance;
- both `_export/strings.txt` and `_export/quick_strings.txt`
  resolution for named string inputs.

It does not run a builder, import a generated module, mutate a source
fragment, or rewrite any export.

## Register model

The M&B 1.011 engine exposes string registers through `s127`, while the
formatter accepts only two digits in a `{sN}` placeholder. Thus `s100-s127`
are valid engine scratch registers but must be copied into `s0-s99` before
being interpolated. A raw integer in a string-register operand is interpreted
as that register (for example `100` means `s100`).

An operand such as `:selector` or `$current_string_reg` can intentionally
select a source string register at runtime. The checker reports that as an
explicit, source-mapped dynamic boundary rather than falsely declaring the
operation malformed. In a branch-free lexical block it proves simple
`assign`, arithmetic, and `store_random_in_range` bounds (for example
`:selector` -> `s11-s14`); cross-menu/global selectors remain warnings until
their runtime range is traced.

Generated M&B modules encode zero-argument operations such as `try_begin`,
`else_try`, and `try_end` as bare Python names. The checker accepts only the
engine-header-derived set of valid bare operations, so data identifiers such as
`anyone` or `trp_player` cannot be mistaken for control flow.

Some generated scripts are assembled by zero-argument local builder functions
instead of a literal operation list. The checker reads those builders' ASTs
without importing or executing generated Python, so an exported helper such as
`sod_get_center_modifier` is analyzed as runtime script content rather than
misreported as a missing script.

The operation behavior is cross-checked against the
[Mount&Blade Modding Wiki string-register reference](https://mbmodwiki.github.io/String_register)
and the [documented operation notes](https://mbcommands.fandom.com/wiki/Operations).

## CLI

Run from the module root:

~~~powershell
py -3 devkit\string_integrity\string_integrity.py summary
py -3 devkit\string_integrity\string_integrity.py summary --format markdown
py -3 devkit\string_integrity\string_integrity.py sinks --kind dialogue --register 5 --include-clean
py -3 devkit\string_integrity\string_integrity.py sinks --query "past_life" --limit 20
py -3 devkit\string_integrity\string_integrity.py summary --output devkit\output\string-integrity.json
~~~

JSON is the default. `sinks` returns non-clean results by default; pass
`--include-clean` to inspect all matches for a phrase, category, or register.
Output is refused beneath `_export/`.

## Interpretation

- **error** — a statically impossible register use, such as a formatter
  placeholder beyond `s99`, or a direct non-register operand passed to
  `str_store_string_reg`.
- **warning** — an unbounded dynamic selector, a clear-before-display
  sequence, or an unresolved script that may overwrite a relevant volatile
  register.
- **info** — a selector proven to a valid local range, or a writer that exists
  outside the current lexical/generated analysis boundary; neither is proof of
  a defect.

The analyzer remains conservative around branches, engine state, and dynamic
selectors. It is designed to identify the smallest source-mapped next
investigation, not to invent runtime certainty.

## Verify

~~~powershell
py -3 -B devkit\string_integrity\test_string_integrity.py
~~~
