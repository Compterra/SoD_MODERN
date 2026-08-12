# Text Execution Ledger

This slice answers the semantic question the compiler and the game normally
cannot:

> Why can this dialogue, menu, overlay, or message render this text?

It is a read-only, LLM-first execution model over generated M&B 1.011 modules.
For a selected visible text sink, it returns:

- the generated sink and modular source provenance;
- the condition/control operation timeline evaluated before display;
- string-register writers and static substitution candidates;
- bounded dynamic-selector ranges where they can be proven;
- static `call_script` string effects and unresolved-call boundaries;
- cross-screen global-variable reads/writes;
- menu inbound/outbound transition evidence; and
- the relevant `strings.txt` or `quick_strings.txt` resolution.

It does not import generated modules, run the builder, mutate source, or write
under `_export/`.

## Start here

The primary interface is MCP:

1. Call `string_integrity` to identify a suspect sink or selector.
2. Call `text_explain` with a phrase or stable sink ID.
3. Use `register_history` when the explanation reads a global/local whose
   writer is outside the current screen.
4. Use `possible_texts` when a dynamic selector may choose several valid
   strings.

For example, `text_explain(query="past_life", kind="menu")` shows the
`{s3}` menu sink, its `$current_string_reg` selector, every known writer of
that global, and the menu's self-loop. `text_explain(query="bandit_attack",
kind="dialogue")` proves that `:rand` selects one of `s11-s14` and
returns the four exact candidate lines.

## CLI

Run from the module root:

~~~powershell
py -3 devkit\text_execution_ledger\text_execution_ledger.py summary
py -3 devkit\text_execution_ledger\text_execution_ledger.py explain --query "past_life" --kind menu
py -3 devkit\text_execution_ledger\text_execution_ledger.py history "$current_string_reg"
py -3 devkit\text_execution_ledger\text_execution_ledger.py possible-texts --query "bandit_attack" --kind dialogue
py -3 devkit\text_execution_ledger\text_execution_ledger.py explain --sink-id "sink:compile/module_game_menus.py:2070:0:menu_text:0"
py -3 devkit\text_execution_ledger\text_execution_ledger.py summary --format markdown --output devkit\output\text-execution-ledger.md
~~~

JSON is the default. `explain` and `possible-texts` include clean sinks by
default because an apparently clean line may still be the line the developer
needs to explain. Pass `--only-non-clean` to focus on warnings/errors.

The process keeps an in-memory cache keyed to generated-module/export
timestamps, so related MCP calls share one immutable index until those inputs
change.

## What it proves and what it does not

The ledger understands generated bare zero-argument control operations such as
`try_begin`, `else_try`, and `try_end`. It reports them explicitly;
it does not pretend to choose one branch without runtime inputs.

It can prove simple lexical dynamic selector ranges, but a global or
cross-screen value remains an evidence boundary until its writer history and
game state are checked. A reported candidate is therefore an explanation
surface, not a claim that every candidate is reachable in one playthrough.

## Verify

~~~powershell
py -3 -B devkit\text_execution_ledger\test_text_execution_ledger.py
~~~
