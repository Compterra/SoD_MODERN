# Quest system architecture audit

## Scope

This audit maps the current `sod_modern` quest system against the 108 reference pattern and identifies every gameplay seam that matters for a future rebuild.

Sources reviewed for this audit:
- `src/quests/quest_schema.py`
- `src/quests/quest_runtime.py`
- `src/quests/0001_prison_break_chain.py`
- `src/quests/0009_story_and_meta_quests.py`
- `src/quests/_preamble/00_schema_helpers.py`
- `src/quests/_preamble/01_runtime_helpers.py`
- `src/quests/_order_quests.txt`
- `build/build_quests.py`
- `docs/quests/quest_framework_overview.md`
- `docs/quests/quest_state_storage_audit.md`
- `docs/quests/runtime_event_audit.md`
- `docs/quests/quest_authoring_audit.md`
- search results across `src/` for quest hooks, slot use, dialogue branches, menus, triggers, and mission templates

This document is intended to be the source of truth for the next quest-system rebuild phase.

---

## 1. Current quest fragment inventory

The current quest content lives under `src/quests/` as modular fragments.

### Fragment list and style

#### `src/quests/0001_all_quests.py`
- Legacy aggregator stub only.
- No quest content.
- Exists as a compatibility marker that points authors toward numbered fragments.

#### `src/quests/0001_prison_break_chain.py`
- **Style:** schema-backed authoring.
- Uses `quest_chain()` and `quest_single_stage_quest()`.
- Represents the first successful conversion away from raw tuple lists.
- Demonstrates the new `QuestBlueprint`/`QuestChain` lowering path.

#### `src/quests/0002_mercenary_guild_quests.py`
- **Style:** legacy tuple fragment.
- Still expected to export `QUESTS = [...]`.

#### `src/quests/0003_lord_quests.py`
- **Style:** legacy tuple fragment.

#### `src/quests/0004_enemy_lord_quests.py`
- **Style:** legacy tuple fragment.

#### `src/quests/0005_army_quests.py`
- **Style:** legacy tuple fragment.

#### `src/quests/0006_lady_quests.py`
- **Style:** legacy tuple fragment.

#### `src/quests/0007_mayor_quests.py`
- **Style:** legacy tuple fragment.

#### `src/quests/0008_village_elder_quests.py`
- **Style:** legacy tuple fragment.

#### `src/quests/0009_story_and_meta_quests.py`
- **Style:** mixed / transitional.
- Uses schema-backed constructs.
- Demonstrates the newer authoring direction while preserving legacy output compatibility.

### Framework support files

#### `src/quests/quest_schema.py`
- Authoring layer.
- Defines:
  - `QuestStage`
  - `QuestBlueprint`
  - `QuestChain`
  - helper constructors such as `quest_stage()`, `quest_blueprint()`, and `quest_chain()`
  - convenience wrappers like `quest_single_stage_quest()`, `quest_delivery_quest()`, `quest_hunt_quest()`, `quest_escort_quest()`, and `quest_rescue_quest()`

#### `src/quests/quest_runtime.py`
- Runtime layer.
- Defines:
  - `QuestProgressEvent`
  - `QuestStageRuntime`
  - `QuestRuntime`
  - `QuestJournal`
  - lifecycle and stage-handling helpers

#### `src/quests/_preamble/00_schema_helpers.py`
- Injects schema helpers into generated quest output.

#### `src/quests/_preamble/01_runtime_helpers.py`
- Injects runtime helpers into generated quest output.

#### `build/build_quests.py`
- Quest fragment compiler.
- Collects modular fragments and merges them into the generated quest module.
- Enforces duplicate quest ID checks.

### Current inventory summary

The quest system is no longer purely legacy, but it is still split across:
- legacy tuple fragments
- schema-backed fragments
- runtime helpers
- build-time lowering to legacy compiler output

That means the system is architecturally halfway modernized, but not yet operationally unified.

---

## 2. Quest entry points in gameplay systems

The quest framework is already touched by many gameplay systems. These are the key entry points that currently read or mutate quest state.

### Triggers

#### `src/triggers/ST01_every_frame/entry_0078.py`
- Continuous frame-based map-distance or progress checks.
- Uses quest activity and slot checks to track proximity and movement-related progress.

#### `src/triggers/ST02_every_hour/entry_0073.py`
- Hourly failure and movement checks.
- Handles quest-related map events and failure states.

#### `src/triggers/ST02_every_hour/entry_0076.py`
- Hourly quest offer / assignment logic.
- Uses active quest checks to avoid conflicting assignments.

#### `src/triggers/ST02_every_hour/entry_0077.py`
- Hourly quest generation and assignment for army quest flow.
- Writes many quest slots during quest creation.

#### `src/triggers/ST02_every_hour/entry_0081.py`
- Periodic active quest tracking.
- Monitors ongoing quest progress conditions.

#### `src/triggers/ST02_every_hour/entry_0082.py`
- Map-state quest tracking for active quests during travel and movement.

#### `src/triggers/ST02_every_hour/entry_0083.py`
- Quest stage or state initialization for long-running quest flows.

#### `src/triggers/ST02_every_hour/entry_0084.py`
- Long-running collection quest state update.
- Example of incremental progress accumulation.

#### `src/triggers/ST03_daily/entry_0075.py`
- Quest expiration and cooldown decrement logic.

#### `src/triggers/ST03_daily/entry_0151.py`
- Threat-board quest progression and claim-readiness handling.

### Menus

#### `src/menus/centers/village/village_bandits_defeated_accept_03.py`
- Quest branching and conclusion logic tied to village quests.

#### `src/menus/village/cattle_herd.py`
- Gate checks for cattle-related quest movement.

#### `src/menus/start_game/start_collecting.py`
- Quest state initialization during game start.

#### `src/menus/start_game/peasant_start_practice.py`
- Quest progress logic tied to practice or training flow.

#### `src/menus/centers/common/approach_gates.py`
- Encounter and travel gating based on quest state.

#### `src/menus/other/continue_23.py`
- Quest-related encounter and consequence branching.

#### `src/menus/0000_hardcoded_mb1011/simple_encounter.py`
- Quest-aware encounter gating and combat interaction control.

### Dialogues

Representative quest/dialogue touchpoints include:

#### Quest acceptance and start
- `src/dialogs/ZZ99_misc_dialogs/anyone_gm_mission_deliver_message_accepted.py`
- `src/dialogs/ZZ99_misc_dialogs/anyone_gm_good_guys_accepted.py`
- `src/dialogs/ZZ99_misc_dialogs/anyone_gm_jc_competition_accepted.py`
- `src/dialogs/ZZ99_misc_dialogs/anyone_gm_mission_raise_troops_accepted.py`
- `src/dialogs/ZE01_companions_and_named_npcs/anyone_gm_mission_hunt_down_fugitive_accepted.py`

#### Quest completion / turn-in
- `src/dialogs/ZZ99_misc_dialogs/anyone_convince_accept.py`
- `src/dialogs/ZZ99_misc_dialogs/anyone_gm_deliver_grain_thank.py`
- `src/dialogs/ZZ99_misc_dialogs/anyone_gm_deliver_horses_thank.py`
- `src/dialogs/ZZ99_misc_dialogs/anyone_tavernkeeper_deliver_wine.py`
- `src/dialogs/ZZ99_misc_dialogs/anyone_tavernkeeper_smuggle_wine.py`
- `src/dialogs/ZZ99_misc_dialogs/anyone_capture_enemy_hero_thank.py`

#### Quest-specific dialogue gating and presentation
- `src/dialogs/ZZ99_misc_dialogs/anyone_convince_begin.py`
- `src/dialogs/ZZ99_misc_dialogs/anyone_convince_accept_06.py`
- `src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_tavernkeeper_talk.py`
- `src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_tavernkeeper_talk_02.py`
- `src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_tavernkeeper_talk_03.py`
- `src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_kidnapped_girl_quest_brief.py`
- `src/dialogs/ZE01_companions_and_named_npcs/anyone_lost_kidnapped_girl_3.py`

### Scripts

#### Quest-like helper workflows
- `src/scripts/ZY_helper_scripts/sod_threat_board_generate_offers.py`
- `src/scripts/ZY_helper_scripts/sod_threat_board_accept_contract.py`
- `src/scripts/ZY_helper_scripts/sod_threat_board_normalize_center.py`
- `src/scripts/ZY_helper_scripts/sod_threat_board_spawn_target.py`
- `src/scripts/ZY_helper_scripts/sod_threat_board_note_party_defeated.py`
- `src/scripts/ZY_helper_scripts/sod_threat_board_complete_contract.py`
- `src/scripts/ZY_helper_scripts/sod_threat_board_fail_contract.py`
- `src/scripts/ZY_helper_scripts/sod_threat_board_describe_active_contract.py`
- `src/scripts/ZY_helper_scripts/sod_threat_board_describe_offer.py`
- `src/scripts/ZY_helper_scripts/sod_threat_board_init_registry.py`

#### Other quest-related helpers
- `src/scripts/ZZ_common_array_processing/spawn_bandits.py`
- `src/scripts/ZZ_common_array_processing/fgtq_end.py`

### Mission templates

#### `src/mission_templates/0042_jotnar_clan_arena/jotnar_clan_arena.py`
- Mission-level quest state mutation and reward adjustment.
- A strong example of battle/mission integration that directly touches quest state.

---

## 3. Current state storage map

The quest system uses a mixed state model across quest objects, NPCs, parties, and globals.

### Authoritative quest state
Primary storage:
- `slot_quest_*`

Used for:
- active/completed/failed/aborted state
- target party / center / troop references
- counters
- deadlines and cooldowns
- rewards
- claim readiness
- stage and chain progress

### NPC / giver memory
Primary storage:
- `slot_troop_*`

Used for:
- quest availability memory
- offer cooldowns
- dialogue gating
- last interaction markers
- chain follow-up state
- local presentation memory

### Party / center / world state
Primary storage:
- `slot_party_*`

Used for:
- active target parties
- quest-linked centers
- threat state
- encounter relevance
- cleared / defeated markers
- world-object flags

### Global / temporary state
Used for:
- offer pools
- scratch generator values
- current target selection
- temporary progress mirrors
- cross-system bookkeeping

### Current problem
The same meaning is often mirrored in multiple storage locations. That causes:
- state duplication
- stale values
- extra cleanup burden
- unclear authority boundaries
- difficult migration to a runtime-driven system

---

## 4. Dependency chart

This section summarizes where quest data is read or mutated.

### Authoring path
1. `src/quests/*.py`
2. `build/build_quests.py`
3. `compile/module_quests.py`
4. generated legacy quest tuples

### Runtime/state path
1. gameplay script / trigger / dialogue / mission
2. `quest_get_slot` / `quest_set_slot`
3. quest-specific progression or lifecycle logic
4. optional journal / UI text updates

### Common mutations
- `script_start_quest`
- `script_succeed_quest`
- `script_fail_quest`
- `script_abort_quest`

### Common reads
- `check_quest_active`
- `check_quest_concluded`
- `quest_slot_eq`
- `quest_get_slot`

### Common write surfaces
- `quest_set_slot`
- troop/party slot writes that mirror quest state
- global variable updates for generators and temporary state

### Current dependency structure
The current system is not centered around the new runtime model yet. Instead, many gameplay systems still mutate slots directly and treat the quest object as a shared database row.

That works, but it is the main barrier to a stronger quest engine.

---

## 5. Gap analysis versus 108

The 108 reference is still stronger in actual gameplay integration. The current project is stronger in architecture direction, but it is not yet as complete.

### 5.1 Quest generation
**108 is better at:**
- generating quests dynamically from world conditions
- tying generation to faction, settlement, and NPC context

**Current gap:**
- generation is present in pieces, but not unified into one runtime-driven system
- generated offer state is scattered across quest, giver, party, and globals

### 5.2 Quest acceptance
**108 is better at:**
- making accept/start logic feel like a cohesive lifecycle event

**Current gap:**
- acceptance still happens through isolated dialogue/menu/script paths
- there is no single runtime event contract for accept flow

### 5.3 Live progression
**108 is better at:**
- reacting continuously to travel, combat, and mission state

**Current gap:**
- live progression is distributed across triggers and scripts
- stage transitions are not yet modeled as first-class runtime events

### 5.4 Battle hooks
**108 is better at:**
- tying battle outcomes into quest progression directly

**Current gap:**
- battle-related updates exist, but they are not unified under one dispatcher
- battle outcomes still rely heavily on ad hoc slot mutation

### 5.5 Completion / failure
**108 is better at:**
- clear distinction between completion, failure, and abort

**Current gap:**
- legacy scripts still mix end-state behavior with cleanup behavior
- terminal transitions are not yet fully standardized

### 5.6 Rewards / consequences
**108 is better at:**
- making quest outcomes influence the campaign more directly

**Current gap:**
- reward and consequence logic is present, but not fully normalized
- different quest families encode rewards differently

### 5.7 Quest expiration
**108 is better at:**
- reliable deadline handling

**Current gap:**
- expiration exists in daily trigger logic, but not as part of a unified runtime lifecycle

### 5.8 Quest chains
**108 is better at:**
- operating as chain-based quest content with progression memory

**Current gap:**
- schema-backed chains now exist, but most content is still legacy and linear
- branching and advanced chain helpers are still missing

### 5.9 NPC dialogue integration
**108 is better at:**
- quest-aware dialogue that reflects active, pending, and completed states

**Current gap:**
- dialogue does many of the right things, but it is not driven by a single runtime contract
- giver memory and quest state are still too entangled

---

## 6. What is already good

The current project already has some strengths that should be preserved.

### Better engineering direction than 108
- schema-backed authoring is much cleaner than raw tuple-only quest definitions
- runtime objects exist explicitly in Python
- modular quest fragments are easier to maintain than one monolithic file
- the build pipeline is already working
- the framework is now documented

### Better future extensibility
- helper constructors exist for common quest shapes
- runtime and schema are separated from generated output
- the architecture can support a real quest DSL

---

## 7. What must be built next

Based on the audit, the next rebuild should focus on these foundational shifts:

### 1. Canonical quest state model
Define one authoritative state schema for quests, stage tracking, targets, deadlines, and completion conditions.

### 2. Unified event vocabulary
Introduce one runtime event contract for:
- map travel
- battle
- mission
- dialogue
- hourly trigger
- daily trigger
- frame trigger
- quest accept
- quest progress
- quest complete
- quest fail
- quest abort

### 3. Storage discipline
Separate:
- authoritative quest state
- NPC memory
- world/party mirrors
- temporary generator state

### 4. Runtime integration
Wire `QuestRuntime` into the gameplay surfaces that already exist.

### 5. Better authoring DSL
Expand schema helpers for:
- branching
- optional stages
- timed stages
- reward/failure bundles
- reusable quest patterns

### 6. Validation
Add checks for:
- chain integrity
- transition validity
- stage reachability
- missing references
- stale mirrors
- duplicate logic paths

### 7. Migration
Keep legacy tuple compatibility while converting the rest of the quest library incrementally.

---

## 8. Priority seams for implementation

The most valuable places to integrate the new system first are:

1. `src/triggers/ST02_every_hour/entry_0077.py`
2. `src/triggers/ST02_every_hour/entry_0083.py`
3. `src/triggers/ST01_every_frame/entry_0078.py`
4. `src/triggers/ST02_every_hour/entry_0081.py`
5. `src/triggers/ST02_every_hour/entry_0082.py`
6. `src/triggers/ST02_every_hour/entry_0084.py`
7. `src/triggers/ST03_daily/entry_0075.py`
8. `src/triggers/ST03_daily/entry_0151.py`
9. `src/menus/0000_hardcoded_mb1011/simple_encounter.py`
10. `src/mission_templates/0042_jotnar_clan_arena/jotnar_clan_arena.py`
11. quest-accept dialogue nodes
12. quest-turn-in dialogue nodes
13. quest-failure / abort branches

---

## 9. Conclusion

The quest system is no longer a blank slate. It already has:
- modular content
- a schema layer
- a runtime layer
- working build integration
- real gameplay touchpoints

But it is still missing the one thing that turns a framework into an engine:
- one coherent authoritative quest lifecycle that all gameplay systems obey.

This audit is the baseline for the rebuild.


