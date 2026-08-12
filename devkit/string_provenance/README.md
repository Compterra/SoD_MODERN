# Interprocedural String Provenance

`string_provenance/` turns the conservative “a script might overwrite this
register” boundary into source-mapped call-chain evidence. It parses generated
`compile/module_scripts.py`, follows literal `call_script` edges, and preserves
the `try`/`else_try` branch conditions surrounding each string-register writer.

```powershell
py -3 -B devkit\string_provenance\string_provenance.py summary
py -3 -B devkit\string_provenance\string_provenance.py paths script_sod_black_khergits_update_horde_state --register s68
py -3 -B devkit\string_provenance\string_provenance.py explain --query "Black Khergit" --limit 3
```

No writer path and no unresolved boundary proves that the selected literal
script graph contains no writer for that register. A returned writer path is a
static possibility, not an assertion that a save-state branch ran. Dynamic
script calls, opaque generated builders, recursion, and depth cutoffs stay
visible as unresolved boundaries.
