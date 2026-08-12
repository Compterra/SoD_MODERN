# Content Forge

Content Forge is the DevKit's LLM-first authoring layer for content that spans
multiple M&B 1.011 systems. A typed JSON pack carries the creative brief and
the technical contract together:

- summary, lore constraints, tone, and testable acceptance criteria;
- dialogue beats and first-match-aware dialogue changes;
- quest/event timelines and typed scripts, quests, menus, mission callbacks;
- campaign AI contracts for stationary camps, patrol radii, escorts, raid
  returns, and despawns;
- direct existing troop/item balance-record edits; and
- presentation layout edits, static canvases, and typed new-presentation
  creation.

It is an orchestration compiler, not a generic editor. Every source mutation
is delegated to the existing specialist that already understands its failure
mode: Feature Authoring/Module Atlas, Dialogue Composer, Presentation Layout,
or Balance Lab. There is no raw Python expression or tuple source field.

## Primary workflow

Use MCP first:

1. `content_forge_summary` and `content_pack_find`
2. `content_pack_explain` and `content_pack_validate`
3. `content_pack_plan` and `content_pack_review`
4. `content_pack_apply` for one named change, dry-run first
5. `content_pack_verify`, then the ordinary reviewed module build

The Windows JSON CLI is equivalent:

```powershell
./devkit/SoDDev.bat content summary
./devkit/SoDDev.bat content explain --pack-id black-khergit-camp-runtime
./devkit/SoDDev.bat content plan --pack-id black-khergit-camp-runtime
./devkit/SoDDev.bat content review --pack-id black-khergit-camp-runtime
./devkit/SoDDev.bat content verify --pack-id black-khergit-camp-runtime --run-scenarios
```

The CLI prints JSON to stdout and writes no artifacts. Inline packs are passed
with `--pack`; checked-in JSON files passed with `--pack-file` must remain
inside `devkit/content_forge/`.

## Human-facing content workspace

The optional local [Module Studio](../module_studio/README.md) now includes a
**Content Forge Studio** page. It is a convenience layer over this exact
contract, not a separate content system. It can:

- browse checked-in packs and load one as a local typed draft;
- edit the player-facing brief, lore/tone/acceptance criteria, verification
  obligations, and all five Content Forge slices;
- show dialogue beats, quest/event progression, AI intent evidence, balance
  rationale, and bounded static presentation canvases together;
- render the deterministic dependency/review canvas and one-specialist-change
  source plans; and
- save a new or revised pack contract only through a separate catalog diff,
  SHA rehearsal, and explicit `SAVE CONTENT PACK` confirmation.

Start it with `./devkit/SoDDev.bat studio`. It binds only to
`127.0.0.1` and has no build/export button or generic filesystem editor.

### Pack catalog save boundary

Normally an agent writes a pack proposal to a local JSON draft or asks the
Studio to stage one visually. The narrow persistence path is available for a
strict checked-in authoring contract:

1. `content_pack_catalog_plan` / CLI `catalog-plan` validates the complete
   pack and returns a unified diff for **only** `devkit/content_forge/packs.json`.
2. `content_pack_catalog_apply` / CLI `catalog-apply` rehearses the exact
   catalog-plan ID and current catalog SHA by default.
3. A real save additionally requires the literal confirmation
   `SAVE CONTENT PACK`.

This save does not apply any content change and never writes `src/`,
`compile/`, `compile/ids/`, `_export/`, or module text exports. After saving,
start the ordinary Content Forge workflow again: explain, validate, plan,
review, then selectively dry-run/apply one specialist change at a time.

## Pack shape

The complete machine contract is
[`contracts/content-pack.v1.schema.json`](contracts/content-pack.v1.schema.json).
The checked-in catalog is [`packs.json`](packs.json).

```json
{
  "schema": "sod-modern.content-pack.v1",
  "id": "example-content",
  "title": "Example Content",
  "status": "draft",
  "description": "What this pack owns.",
  "brief": {
    "summary": "The player-facing goal.",
    "lore_constraints": ["A non-negotiable setting fact."],
    "tone": ["plain and consequential"],
    "acceptance_criteria": ["A source/static or in-game observable result."]
  },
  "slices": {
    "dialogue": {"beats": [], "changes": []},
    "quest_event": {"timeline": [], "changes": []},
    "campaign_ai": {"contracts": [], "scenarios": [], "changes": []},
    "troop_item": {"records": []},
    "presentation": {"screens": [], "changes": [], "new_presentations": []}
  },
  "verification": {
    "tests": ["build/test_example_static.py"],
    "require_blueprint": false,
    "scenarios": []
  }
}
```

All slice keys are optional, but a pack must contain at least one slice. A
slice's `changes` field contains the existing typed Feature Authoring change
body **without** `kind`; Content Forge assigns it from the slice:

| Slice | Delegate | `kind` assigned |
| --- | --- | --- |
| `dialogue` | Dialogue Composer | `dialogue` |
| `quest_event` | Module Atlas via Feature Authoring | `module` |
| `campaign_ai` | Module Atlas via Feature Authoring | `module` |
| `presentation.changes` | Presentation Layout | `presentation` |
| `presentation.new_presentations` | Module Atlas via Feature Authoring | `module`, action `add_presentation` |
| `troop_item.records` | Balance Lab | record-local legacy patch |

This keeps the existing operation IR as the only way to render M&B source.
For example, a source operation is structured JSON such as
`{"op":"assign","args":[{"global":"$g_example"},1]}`, never a freeform
tuple string.

## Order and apply boundaries

Content Forge compiles slices in a stable review order: quest/event, campaign
AI, dialogue, presentation, then troop/item records. That order is a review
sequence, not a fictional transaction. A pack may span many source fragments,
but `content_pack_apply` can apply only one named change at a time. It requires:

- the exact current `content-plan` ID;
- the selected target's current SHA-256;
- for a troop/item record, the selected Balance Lab plan SHA too; and
- the existing explicit legacy acknowledgement for a non-dry troop/item write.

After every non-dry change, refresh the plan. This is deliberate: inserting a
dialogue route can change first-match precedence, and adding a record or
presentation can have order/ID consequences that must be reviewed rather than
silently bundled.

Content Forge never writes `compile/`, `compile/ids/`, `_export/`, or live
module text exports. It also does not add/move troop or item records: those are
ID-sensitive legacy sequences and remain a deliberate order-control decision.

## Campaign AI contracts

Each `campaign_ai.contracts` entry names an existing script entrypoint,
explicit required source markers, and one intent:
`stationary_camp`, `patrol_radius`, `escort_attachment`, `raid_return`, or
`despawn`.

For a new generic contract, supply `party_template` plus the relevant fields
such as `expected_behavior`, radius bounds, `attach_to`, `return_when`, or
`despawn_when`. Content Forge converts it into the existing Campaign State
Doctor's scoped party-AI model. A mature checked-in state contract can instead
be linked with `state_contract_id`, as the Black Khergit pack does.

Planning can report an AI contract as `pending_post_apply_verification` when
the selected source edit is intended to establish the missing contract. A
non-dry apply must be followed by `content_pack_verify`, which reruns the
current-source contract model and optional bounded deterministic scenarios.

## Human review canvas

`content_pack_review` and `content_pack_preview` return a structured review
canvas plus Mermaid flow text. It shows the brief, slices, change sequence, AI
contracts, and acceptance criteria without making a browser-based editor the
authority. A local UI may render that payload, but the exact JSON plan and
specialist SHA guard always remain the source of truth.
