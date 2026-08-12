# Dialogue Inspector

Standalone diagnostics for the Mount & Blade 1.011 dialogue pipeline.  This
tool reads project files; it does not alter `src/`, `compile/`, or `_export/`.

For Codex/LLM usage, prefer the typed read-only tools in
[`../mcp_server/`](../mcp_server/README.md). This CLI remains the deterministic
implementation and a useful fallback for shell-based or offline diagnosis.

It works from the generated `compile/module_dialogs.py`, because the modular
dialogue builder deliberately records the originating fragment above each
entry.  That lets a report show the order the engine sees *and* the source
fragment that produced it.

## Run it

From the module root:

```powershell
py -3 devkit\dialogue_inspector\dialogue_inspector.py summary
py -3 devkit\dialogue_inspector\dialogue_inspector.py routes --state lord_start
py -3 devkit\dialogue_inspector\dialogue_inspector.py routes --contains "company"
py -3 devkit\dialogue_inspector\dialogue_inspector.py text "str_store_string"
py -3 devkit\dialogue_inspector\dialogue_inspector.py text "the company will be paid"
py -3 devkit\dialogue_inspector\dialogue_inspector.py graph --state lord_start --depth 2 --output devkit\output\lord-start.dot
```

`routes` is ordered exactly as `compile/module_dialogs.py`.  This matters:
non-player dialogue chooses the first matching line, while player replies show
all matching lines.  The report therefore makes shadowing and fallback order
visible without asking you to infer it from fragmented source files.

`text` searches the layers that matter when text appears in the wrong place:

1. modular source under `src/`;
2. generated `compile/module_dialogs.py` and `compile/module_strings.py`;
3. exported `strings.txt`, `quick_strings.txt`, and `conversation.txt`.

It accepts ordinary case-insensitive text by default and treats underscores in
exports as spaces, so an in-game phrase can be traced into `strings.txt` or
`quick_strings.txt`. Add `--regex` for a regular expression or
`--case-sensitive` for an exact-case search. `--limit` is a cap per pipeline
layer; use `--limit 0` to remove it.

`graph` emits DOT to standard output unless `--output` is supplied.  DOT is a
plain-text graph format; if Graphviz is installed, render it with:

```powershell
dot -Tsvg devkit\output\lord-start.dot -o devkit\output\lord-start.svg
```

The inspector warns when `compile/module_dialogs.py` is older than modular
dialogue source.  Regenerate the compiled module first when that happens:

```powershell
py -3 build\build_dialogs.py
```

Then inspect the generated order before running the full export build.  This
keeps the DevKit outside the build pipeline while still supporting pre-export
diagnosis.

## Safety boundaries

- Output is read-only unless `graph --output` is explicitly requested.
- The tool refuses to write under `_export/`.
- No third-party Python package is required.

## Verify this slice

```powershell
py -3 devkit\dialogue_inspector\test_dialogue_inspector.py
```
