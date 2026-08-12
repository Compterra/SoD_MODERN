# SoD Module Studio

`module_studio/` is the optional, CBO-style local viewer/editor slice of the
SoD Modern DevKit. It is deliberately *not* the primary interface: Codex/LLM
clients should continue to use MCP and deterministic JSON CLIs. Studio simply
puts the same bounded evidence and semantic authoring paths behind a local
screen when a human wants to sort, compare, and review work visually.

## Start it

From the module workspace:

```powershell
.\devkit\SoDDev.bat studio
```

or:

```powershell
py -3 -B devkit\module_studio\module_studio.py serve
```

It binds only to `http://127.0.0.1:8797/`, prints the URL, and never opens a
browser automatically. A different local port is fine:

```powershell
.\devkit\SoDDev.bat studio --port 8801
```

`--host` cannot be changed. Studio rejects non-loopback binds, accepts only
loopback clients, does not send CORS headers, and never calls the network.

For machine-readable discovery without starting a server:

```powershell
py -3 -B devkit\module_studio\module_studio.py catalog
py -3 -B devkit\module_studio\module_studio.py summary
```

## What it exposes

| Surface | Existing DevKit authority it presents |
| --- | --- |
| Module Atlas | Search all eight source areas; entity context, source/generated provenance, menu/script/mission flow, trigger/quest/references, and bounded dependency graphs. |
| Dialogue | Authored route search, source/compiled-order evidence, and static first-match/fallback analysis. |
| Presentation Workshop | Browse or search a presentation, inspect its direct overlay canvas, select/list overlays, locally drag a static anchor, edit numeric position/size/text/mesh/color/alpha or alignment, and create a text/button/mesh/slider overlay through the same guarded plan flow. |
| Content Forge Studio | Browse checked-in content packs; edit a local typed brief and all dialogue, quest/event, campaign-AI, presentation, and troop/item slices; preview player-facing beats/timelines/contracts/static canvases; review the dependency canvas; plan/rehearse one specialist change; and save only a reviewed strict pack contract through a separate catalog SHA gate. |
| Text observability | Workbench text lint for visible-text and string/register risk evidence. |
| Order Control | Source manifest, authored/route, generated-ID, and protected callback-order inspection; anchored move risk, plan, dry-run, and guarded apply. |
| Troop + Item Balance Lab | Evaluated legacy item/troop records, decoded stats, randomized inventory pools, direct upgrade-tree evidence, price/kit outliers, and a record-local guarded balance editor. |
| Workbench | Fixed impact packets, release readiness, and static contracts/scenario context. |
| Guarded editor | `module_patch`, `dialogue_patch`, or `presentation_patch` planning and their respective guarded apply functions. |

The JSON API uses the same paths, such as:

- `GET /api/atlas/find?area=menus&query=...`
- `GET /api/dialogue/context?route_id=...`
- `GET /api/presentation/canvas?presentation_id=...&overlay_limit=500`
- `GET /api/content/summary` and `GET /api/content/explain?pack_id=...`
- `POST /api/content/validate`, `/api/content/plan`, `/api/content/preview`, and `/api/content/review` with one strict inline `pack` object
- `POST /api/content/catalog-plan` and `/api/content/catalog-apply` for the separate checked-in pack-contract persistence gate
- `GET /api/order/explain?target=source:src/...` and `GET /api/order/verify`
- `GET /api/balance/item?item_id=itm_khergit_bow`
- `GET /api/balance/troop?troop_id=trp_swadian_recruit` and `GET /api/balance/outliers?domain=troops`
- `GET /api/workbench/impact?target=...`
- `POST /api/atlas/patch` and `/api/atlas/apply` (with equivalent dialogue, presentation, anchored order-move, and balance-record routes)

Run `catalog` or `GET /api/catalog` for the complete endpoint list and the
exact safety contract. Results are JSON envelopes, so a local agent can use
Studio's service without scraping the visual UI.

## Editing contract

The Studio cannot issue raw file edits. It accepts only named semantic fields
supported by the Atlas, specialist Dialogue/Presentation composers, Order
Control's deliberately narrow anchored-move contract, or the Balance Lab's
direct legacy item/troop record contract.

1. A `POST .../patch` request is read-only and returns a unified diff and the
   current target SHA-256.
2. A matching `POST .../apply` defaults to `"dry_run": true`.
3. A real apply additionally requires that exact current SHA and
   `"confirmation": "APPLY SOURCE"`.
4. Normal applies write one guarded modular source fragment only. They never
   build or overwrite `_export/`. The one deliberate compatibility exception is
   `POST /api/balance/apply`: after build-route confirmation, its source SHA,
   plan SHA, `APPLY SOURCE` confirmation, and explicit legacy-authoring
   acknowledgement, it may write exactly one direct record in
   `compile/module_items.py` or `compile/module_troops.py`. It cannot add/move
   records or write `compile/ids`, generated files, or exports.
5. Referenced Atlas removals need their own exact acknowledgement:
   `"removal_acknowledgement": "REMOVE REFERENCED ENTITY"`.

Content Forge Studio follows the same source/apply rule for a selected
specialist content change. Its visual draft has a separate, intentionally
narrow persistence route: after a reviewed catalog diff and dry-run,
`POST /api/content/catalog-apply` can write exactly one strict pack contract
to `devkit/content_forge/packs.json` only when
`"confirmation": "SAVE CONTENT PACK"`. It cannot write `src/`, `compile/`,
generated IDs, exports, or any arbitrary file. Saving a pack contract does not
apply its module changes; validate/plan/review those independently afterward.

For order work, Studio can move only two source fragments governed by the same
declared `_order*.txt` manifest or two dialogue routes in one source fragment.
A source-fragment apply writes that manifest only; it does not rename a folder,
move a file, hand-edit `compile/ids`, build, or write an export.
An active protected engine/legacy contract also needs the deliberate
`allow_protected_contract_change` acknowledgement in addition to the normal
`APPLY SOURCE` confirmation.

For a Balance Lab hardwired record, Studio additionally asks for the protected
legacy-record acknowledgement. Derived upgrade variants remain view-only;
their runtime records have no direct source field to patch.

After a real source change, use the ordinary reviewed build process and the
target in-game smoke path. Studio's static canvas, text, graph, and dialogue
analysis reduce blind spots; they are not gameplay proof.

### Presentation Workshop workflow

The Presentation page is a dedicated visual authoring surface, not a generic
text editor. Click an overlay on the canvas or in its list to see its source
binding, string-writer evidence, static/dynamic status, and shared-binding
risk. A drag only updates local draft coordinates. It does not send a source
request until **Review move / dragged position** is selected. The stage labels
those drafts, keeps multiple overlay drafts separate, and can reset the
selected draft back to its source anchor. The layer inventory remains in source
order and can be filtered without changing that order.

The same applies to numeric position/size, text or mesh, color/alpha,
alignment, removal, and new-overlay creation: each produces one exact
`presentation_patch` plan and unified diff first. The Workshop then exposes a
dry-run, SHA-bound apply, and the existing `APPLY SOURCE` confirmation. Dynamic
coordinates are shown as unresolved rather than guessed, and a shared `posN`
binding is called out before source apply. Content that is supplied through an
`s` register is deliberately shown as a source expression and its text field
stays disabled: the Workshop will not accidentally replace dynamic content with
the literal characters of a register name. Use the text/string workflow to
change that writer, or intentionally use the lower-level semantic API after
reviewing the plan.

### Content Forge Studio workflow

The Content Forge page is the player-facing content surface that joins the
specialist editors without bypassing them. Start by loading an existing pack
or creating a local draft. The brief form captures the player-facing summary,
lore, tone, acceptance criteria, and verification obligations; slice toggles
and typed JSON rows then describe dialogue beats, event progression, campaign
AI contracts, presentation screens, and direct legacy-record intent.

Use **Preview player-facing content** to see what the player can encounter:
dialogue beat cards, an event timeline, campaign behavior proof, balance
rationale, and bounded static presentation canvases. Use **Review dependency
canvas** to inspect the pack/slice/change/AI graph before source work.

The source-plan panel presents independent named changes from Content Forge;
select one, inspect its exact specialist diff, rehearse it, and use the normal
`APPLY SOURCE` acknowledgement only for that one change. A multi-slice pack is
not treated as an atomic transaction, so re-plan after every non-dry apply.

The catalog panel is deliberately separate. It has a different confirmation,
`SAVE CONTENT PACK`, and affects only `devkit/content_forge/packs.json`. This
makes it safe to persist an authored-content contract without accidentally
changing the module while a human is organizing player-facing work.

## Test

```powershell
py -3 -B devkit\module_studio\test_module_studio.py
```

The test creates an isolated miniature module, calls viewer endpoints, plans a
semantic menu edit, proves the SHA dry-run leaves source intact, and proves a
real apply is refused without explicit confirmation.
