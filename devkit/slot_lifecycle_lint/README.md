# Slot Ownership + Lifecycle Lint

`slot_lifecycle_lint/` makes the shared-memory side of the M&B 1.011 module
system explicit. It reads the Campaign State Doctor's source-mapped state
accesses and a checked-in ownership catalog; it never imports module source,
builds the module, or writes exports.

It detects:

- a declared slot written by a script outside its owning subsystem;
- lifecycle-bound slots that are set but never cleared to their declared reset
  value;
- a same-path read after a literal clear; and
- undeclared multi-system writers as an information-level review candidate.

The important distinction is deliberate: naming is not proof of ownership.
Only checked-in rules produce ownership failures, and only rules with
`require_clear: true` treat an absent clear as an error.

Rules may name an exact `slot_names` list for a lifecycle contract, or one
`slot_prefix` for a true subsystem namespace. Use exact names for token/cache
slots whose invalidation does not mean writing zero; a broad prefix with
`require_clear` would otherwise create a misleading error for every cache.

```powershell
py -3 -B devkit\slot_lifecycle_lint\slot_lifecycle_lint.py summary
py -3 -B devkit\slot_lifecycle_lint\slot_lifecycle_lint.py ownership black_khergit
py -3 -B devkit\slot_lifecycle_lint\slot_lifecycle_lint.py slot slot_party_black_khergit_origin
```

The JSON/MCP surface is the primary interface. The checked-in
[`ownership.json`](ownership.json) catalog is the reviewable source of truth
for actual subsystem ownership and approved conversion handoffs.
