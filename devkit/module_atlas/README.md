# Module Atlas

The Module Atlas is the DevKit's LLM-first control plane for the entire
Mount & Blade 1.011 modular module system. It statically parses source; it
does **not** import or execute the legacy module data.

It indexes the eight authored source areas as semantic entities:

| Area | Entity model | Specialist view |
| --- | --- | --- |
| `constants` | named assignments | `entity_references` |
| `dialogs` | first-match dialogue routes | Dialogue Composer |
| `menus` | menus and selectable options | `menu_flow` |
| `mission_templates` | mission templates and event/timed triggers | `mission_timeline` |
| `presentations` | presentation records | Presentation Layout Composer |
| `quests` | quest records | `quest_registry` |
| `scripts` | callable operation blocks | `script_flow` |
| `triggers` | simple interval/event operation blocks | `trigger_timeline` |

The Atlas is intentionally not a generic file editor. Its semantic actions
compile into exact Change Router anchors. A plan is read-only; `apply` requires
the plan's current SHA-256 and defaults to rehearsal mode. It writes only the
chosen `src/**/*.py` fragment, never `compile/` or `_export/`.

## Recommended agent workflow

1. Run `summary`, then `integrity` before assuming a reference is broken.
2. Use `find` to obtain an Atlas entity ID, then `context` and `graph` to see
   ownership, generated provenance, direct static callers, callees, children,
   and supported actions.
3. Use a specialist view when one exists: `menu-flow`, `script-flow`,
   `mission-timeline`, `trigger-timeline`, `quest-registry`, or `references`.
4. Create a `patch` plan, inspect its exact unified diff and relationship
   evidence, then pass its SHA to `apply` with the default dry-run first.
5. Run `verify` after a real apply, then intentionally use the normal build
   pipeline when ready to refresh generated modules and exports.

Dialogue and presentation records appear in Atlas search/context/graphs, but
their authoring is deliberately delegated to `dialogue_patch` and
`presentation_patch`. That preserves dialogue first-match/shadow analysis and
presentation overlay/register-layout semantics instead of flattening them into
unsafe generic edits. The one narrow presentation exception is
`add_presentation`: it appends a wholly new typed presentation at a named
existing presentation append anchor. Existing screen layout changes still
belong to Presentation Layout.

## CLI examples

```powershell
py -3 -B devkit\module_atlas\module_atlas.py summary
py -3 -B devkit\module_atlas\module_atlas.py integrity --limit 50
py -3 -B devkit\module_atlas\module_atlas.py menu-flow past_life_explanation
py -3 -B devkit\module_atlas\module_atlas.py script-flow sod_battle_xp_log_start
py -3 -B devkit\module_atlas\module_atlas.py mission-timeline bandits_at_night
py -3 -B devkit\module_atlas\module_atlas.py references sod_migration_prosperity_max
```

All commands emit deterministic JSON. Use `--output devkit/output/name.json`
to save a diagnostic artifact without touching module source.

## Semantic authoring coverage

`module_patch` and `module_apply` support appropriate edits rather than a
single raw text surface:

| Entity | Semantic actions |
| --- | --- |
| constant | change expression; add a nearby constant; guarded removal |
| menu | change text/expressions; add menu/option; edit enter operations; guarded removal |
| menu option | change text/expressions; edit conditions/consequences; remove option |
| mission template | change expressions; add mission/trigger; guarded removal |
| mission trigger | edit condition/consequence blocks, interval, remove trigger |
| presentation | append a new typed presentation only; edit existing overlays/triggers in Presentation Layout |
| quest | change title/description/flags; add quest; guarded removal |
| script | change operation block; add script; guarded removal |
| simple trigger | change operation block/interval; add/remove trigger |

Stable IDs cannot be renamed by a generic action. Create a replacement and
migrate static references deliberately. Likewise, top-level removal refuses
when Atlas sees inbound references unless `allow_referenced_removal` is set in
the plan and apply request; this acknowledgement does not make dynamic paths
safe, it makes the risk explicit.

`integrity` treats references found in generated `compile/ids` as known
base/legacy fallback boundaries rather than false missing-reference failures.
It reports actual unresolved direct script/menu/mission/presentation/quest
references separately. Dynamic engine IDs, strings, and non-Atlas types remain
explicitly outside the static claim.

## Test

```powershell
py -3 -B devkit\module_atlas\test_module_atlas.py
```

The test creates an isolated miniature workspace containing all eight source
areas and proves discovery, graph links, integrity, semantic plans, removal
protection, and dry-run non-mutation.
