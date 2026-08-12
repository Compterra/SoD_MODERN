# Dialogue Reachability Model Checker

`dialogue_model_checker/` is the proof-oriented layer above the existing
compiled-order inspector. It evaluates the real generated `module_dialogs.py`
list in engine order and reports only what its constraint model can establish:

- internally contradictory routes that cannot match;
- NPC routes shadowed by an earlier first-match route;
- NPC route pairs with a proved conditional overlap;
- identical player choices that can lead to different states; and
- authored input states with no engine entry or incoming route; and
- target states whose only authored routes are proved dead.

It understands branch-free equality, inequality, literal integer ranges, slot
comparisons, and exact boolean/script-condition atoms. Dynamic/disjunctive
conditions, `try_begin`/`else_try` flow, loops, and state-changing operations
remain visible as model boundaries rather than being flattened into a false
conjunction. A finding is therefore a proof within the supported core, not a
guess about a complex executable condition block.

```powershell
py -3 -B devkit\dialogue_model_checker\dialogue_model_checker.py summary
py -3 -B devkit\dialogue_model_checker\dialogue_model_checker.py state sod_company_spokesperson_response
py -3 -B devkit\dialogue_model_checker\dialogue_model_checker.py findings --severity error
```

Use the resulting route index with Dialogue Composer or Order Control only
after reviewing the model evidence. This tool does not execute dialogue
condition scripts or certify a save-state path.
