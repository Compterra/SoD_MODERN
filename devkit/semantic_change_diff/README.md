# Semantic Change Diff

`semantic_change_diff/` captures the semantic surfaces that a plain file diff
cannot describe: compiled dialogue precedence, campaign-state writers, visible
string sinks, generated IDs, trigger effects, and all exported `.txt` hashes.

Capture a baseline before an edit, make the source change through the normal
guarded workflow, run the normal reviewed build when generated/export evidence
matters, then compare:

```powershell
py -3 -B devkit\semantic_change_diff\semantic_change_diff.py snapshot --label before-black-khergit-work
py -3 -B devkit\semantic_change_diff\semantic_change_diff.py diff --baseline before-black-khergit-work
```

Baseline files are confined under `devkit/semantic_change_diff/baselines/` and
ignored by Git. The tool never writes source, `compile/`, or `_export/`.
