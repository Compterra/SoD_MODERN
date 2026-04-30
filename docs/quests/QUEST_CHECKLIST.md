# QUEST CHECKLIST

## Status key
- [x] Complete
- [-] In progress / partially complete
- [ ] Not started

## Audit summary
- [x] The quest system is now a real source-backed stack, not a stub.
- [x] The codebase contains distinct layers for domain modeling, runtime state, events, dynamic generation, quest-giver state, diagnostics, DSL helpers, schema exports, and modular content fragments.
- [-] The code is strong at the library layer, but some gameplay integration and final end-to-end wiring are still incomplete.
- [ ] Live gameplay reachability still needs final verification across the whole module stack.

### Audit note
- [x] This checklist reflects the current `src/quests` source tree.
- [x] Items are marked complete only where the code actually implements the feature.
- [-] Items marked partial exist in code but still have obvious integration, coverage, or verification gaps.
- [ ] Open items remain where the codebase still needs live-engine wiring or final validation.

---

## Phase 1 — Audit the quest system against the 108 source
- [-] Map the current system against the 108 source and identify every gameplay seam

### Source inventory
- [x] Quest domain types are present in `src/quests/quest_domain.py`
- [x] Runtime and journal support are present in `src/quests/quest_runtime.py`
- [x] Event model and dispatcher support are present in `src/quests/quest_events.py`
- [x] Event source adapters are present in `src/quests/quest_event_sources.py`
- [x] Dynamic generation support is present in `src/quests/quest_generation.py`
- [x] Quest giver runtime support is present in `src/quests/quest_giver_runtime.py`
- [x] Diagnostics and validation support are present in `src/quests/quest_diagnostics.py`
- [x] DSL/helper support is present in `src/quests/quest_dsl.py`
- [x] Public schema/re-export surface is present in `src/quests/quest_schema.py`
- [x] Migration support is present in `src/quests/quest_migration.py`

### Quest content inventory
- [x] Modular quest fragments exist under `src/quests/`
- [x] The quest fragment order manifest exists at `src/quests/_order_quests.txt`
- [x] Fragment groups are split into readable content sets such as startup, prison break, mercenary guild, lord, enemy lord, army, lady, mayor, village elder, and story/meta content
- [-] A full crosswalk from these fragments to the 108 system still needs final audit notes

### Deliverable status
- [-] The system inventory is mostly complete, but the full written seam analysis is still partially open
- [ ] The final audit report still needs to be published as the single source of truth for the rebuild

### Audit note
- [x] The source inventory is done because the quest package layout is now known.
- [-] The seam crosswalk is only partially done because the code has been identified, but the final 108-side audit writeup is still open.
- [ ] The phase is not fully done until the audit report is published and reviewed.

---

## Phase 2 — Define the quest domain model
- [x] Replace “tuple quests” as the mental model with a proper domain model

### Core types
- [x] `QuestTemplate`
- [x] `QuestChain`
- [x] `QuestStage`
- [x] `QuestOffer`
- [x] `QuestRuntime`
- [x] `QuestJournal`
- [x] `QuestCondition`
- [x] `QuestAction`
- [x] `QuestTrigger`
- [x] `QuestReward`
- [x] `QuestFailure`
- [x] `QuestNPCState`
- [x] `QuestWorldContext`
- [x] `QuestBlueprint`

### Design principles
- [x] Quests are authored as structured objects, not raw tuples
- [x] Runtime state is separate from authored data
- [-] Chains can branch, fail, fork, or resume
- [x] Quest logic is declarative where possible
- [-] Engine-specific script generation happens at build time

### Result
- [x] A quest model capable of representing far more than the old tuple-based structure

### Audit note
- [x] The domain model exists and is implemented in the source tree.
- [-] Some chain/branch behavior is still richer in the data model than in the fully integrated gameplay path.
- [-] Build-time generation exists, but the final engine-side wiring still needs confirmation.

---

## Phase 3 — Build the runtime state machine
- [x] Quest progression state is represented explicitly

### Runtime features
- [x] `QuestStageRuntime`
- [x] `QuestRuntime`
- [x] `QuestJournal`
- [x] `QuestProgressEvent`
- [x] Runtime state constants for active, inactive, completed, failed, aborted, pending
- [x] Stage state management
- [x] Terminal state detection
- [x] Completion and failure transitions
- [x] Stage advancement helpers
- [x] Progress summaries and snapshots
- [x] Journal registration from blueprints
- [x] Journal registration from chains
- [x] Runtime sorting and prioritization helpers
- [x] Category, pinning, and urgent quest handling
- [x] Warning flag normalization
- [x] Capacity and archive tracking
- [x] Event dispatch passthrough from runtime to stage/runtime/quest handlers

### Result
- [x] Quest state can now be tracked as runtime data instead of ad hoc script flags

### Audit note
- [x] The runtime layer is implemented and usable.
- [-] End-to-end gameplay progression still depends on the rest of the module stack.
- [ ] Live integration still needs full verification outside the runtime layer itself.

---

## Phase 4 — Build event-driven quest progression
- [x] Make quests react to the world naturally at the source layer

### Event system
- [x] `QuestWorldEvent`
- [x] `QuestEventDispatchRecord`
- [x] `QuestEventSubscription`
- [x] `QuestEventDispatcher`
- [x] Event dispatch and subscription support
- [x] Event matching and filtering primitives
- [x] Event record/history support
- [x] Source adapter helpers for emitting world events
- [x] Runtime-friendly event dispatch integration

### Event source coverage
- [x] battle start
- [x] battle end
- [x] agent killed
- [x] prisoner captured
- [x] prisoner freed
- [x] party enters center
- [x] conversation started
- [x] conversation ended
- [x] item acquired
- [x] item lost
- [x] relation changed
- [x] faction state changed
- [x] village raided
- [x] center besieged
- [x] mission succeeded
- [x] mission failed
- [x] caravan created
- [x] caravan destroyed
- [x] time passed
- [x] inventory updated

### Result
- [x] The source layer now has a real event system for quest progression

### Audit note
- [x] The event source and dispatcher stack exists.
- [-] Live engine hooks still need full verification in actual gameplay contexts.
- [ ] The phase is not fully finished until the engine is proven to emit these events in play.

---

## Phase 5 — Implement quest-giver and NPC state
- [x] Give NPCs persistent quest-aware state

### State and runtime
- [x] `QuestNPCState`
- [x] `QuestGiverRuntime`
- [x] Quest giver management/runtime layer
- [x] Offer generation support through quest offers
- [x] Quest availability, cooldown, and history tracking
- [x] Quest giver metadata/state serialization support

### Result
- [x] NPCs can hold quest state in the source model

### Audit note
- [x] The quest-giver state layer exists in source.
- [-] The full dialogue-driven gameplay usage still needs end-to-end validation.
- [ ] The phase remains open until the live quest giver interactions are fully wired.

---

## Phase 6 — Build dynamic quest generation
- [x] Generate quests from world state instead of hardcoding every offer

### Generation types and inputs
- [x] `QUEST_GENERATION_TYPES`
- [x] `QUEST_GENERATION_INPUTS`
- [x] `QuestGenerationContext`
- [x] `QuestGenerationRule`
- [x] `DynamicQuestTemplate`
- [x] `GeneratedQuestOffer`

### Generation behavior
- [x] Context coercion and normalization
- [x] Rule validation and applicability checks
- [x] Template scoring by context
- [x] Region and faction-personality weighting
- [x] Required-rule gating
- [x] Difficulty clamping and adjustment
- [x] Offer filtering against recent IDs
- [x] Cooldown handling
- [x] Offer sorting and limiting

### Built-in templates
- [x] `DEFAULT_DYNAMIC_QUEST_TEMPLATES`
- [x] rescue
- [x] escort
- [x] hunt
- [x] delivery
- [x] sabotage
- [x] defense
- [x] diplomacy
- [x] recruitment
- [x] investigation
- [x] revenge
- [x] retaliation
- [x] infiltration
- [x] siege_support
- [x] recovery
- [x] assassination
- [x] relief_supply
- [x] prisoner_exchange

### Result
- [x] The code can generate dynamic quest offers from world-state inputs

### Audit note
- [x] Dynamic quest generation is implemented and source-backed.
- [-] Final balance tuning and gameplay validation still remain open work.
- [ ] The phase is not fully done until the generated quests are proven in live content.

---

## Phase 7 — Expand the authoring DSL and helpers
- [x] Make large quest chains easier to create and maintain

### DSL and helper functions
- [x] `quest_chain(...)`
- [x] `quest_stage(...)`
- [x] `quest_template(...)`
- [x] `quest_blueprint(...)`
- [x] `quest_offer(...)`
- [x] `quest_branch(...)`
- [x] `quest_reward_bundle(...)`
- [x] `quest_failure_bundle(...)`
- [x] `quest_optional_stage(...)`
- [x] `quest_timed_stage(...)`
- [x] `quest_repeatable_stage(...)`
- [x] `quest_condition(...)`
- [x] `quest_action(...)`
- [x] `quest_trigger(...)`
- [x] `quest_reward(...)`
- [x] `quest_failure(...)`
- [x] `quest_single_stage_quest(...)`
- [x] `quest_world_context(...)`
- [x] `delivery_quest(...)`
- [x] `hunt_quest(...)`
- [x] `escort_quest(...)`
- [x] `rescue_quest(...)`
- [x] `siege_quest(...)`
- [x] `diplomacy_quest(...)`
- [x] `ambush_quest(...)`
- [x] `investigation_quest(...)`

### Authoring capabilities
- [x] Reusable stage patterns
- [x] Templated quest families
- [x] Chain composition
- [x] Declarative conditions and actions
- [x] Safe defaults and validation
- [x] A full themed helper library for every quest archetype
- [-] Exhaustive authoring guidance for every advanced edge case

### Result
- [x] The authoring API is large enough to build real quest content

### Audit note
- [x] The core DSL helpers are implemented in source.
- [-] The higher-level content library still has room to grow.
- [ ] The phase is not fully done until the full helper library and usage patterns are finalized.

---

## Phase 8 — Add validation and diagnostics
- [x] Catch bad quest content before it ships

### Validation layers
- [x] Identifier validation
- [x] Duplicate dynamic template ID validation
- [x] Unknown dynamic generation type validation
- [x] Unknown generation input validation
- [x] Impossible generation rule validation
- [x] Impossible generation weight detection
- [x] Missing narrative metadata detection
- [x] Missing stage dialogue detection
- [x] Missing reaction text detection
- [x] Missing battle-line detection
- [x] Missing map-line detection
- [x] Missing quest identifier detection
- [x] Missing battle objective kind detection

### Diagnostics surface
- [x] `QuestDiagnostic`
- [x] `QuestDiagnosticsReport`
- [x] `validate_dynamic_generation_templates(...)`
- [x] `validate_quest_template_graph(...)`
- [x] `validate_quest_chain_graph(...)`
- [x] `diagnose_quest_graph(...)`
- [x] `diagnose_battle_objectives(...)`
- [x] `diagnose_dialogue_branch_coverage(...)`
- [x] `diagnose_quest_narrative(...)`
- [x] `build_quest_diagnostics_report(...)`
- [x] report summarization helpers
- [x] diagnostics-to-dictionary helpers

### What is still missing
- [-] Source line mapping in diagnostics
- [-] Exhaustive conflict reporting across every quest fragment
- [-] Full author-facing build error presentation

### Result
- [x] The build can already explain a lot of quest-content problems
- [-] It does not yet explain every possible problem with perfect source mapping

### Audit note
- [x] Diagnostics and validation are real and implemented.
- [-] They are strong, but not yet the final perfect authoring experience.
- [ ] The phase is not fully done until source mapping and conflict reporting are complete.

---

## Phase 9 — Finalize the public surface and migration story
- [x] Make the quest package importable through a coherent public surface

### Public surface
- [x] `quest_schema.py` exists as a re-export surface
- [x] The domain, specs, generation, DSL, diagnostics, outcomes, and migration layers are exposed through the schema surface
- [x] Module `__all__` exports are defined for the main quest modules
- [x] The source tree has a dedicated migration module

### Remaining concerns
- [-] Backward-compatibility strategy still needs final review
- [-] Final package boundary decisions still need audit confirmation

### Result
- [x] The quest API surface is already structured for consumption

### Audit note
- [x] Public exports are already curated in source.
- [-] The final compatibility story still needs a last pass.
- [ ] The phase is not fully done until the package boundary is finalized.

---

## Phase 10 — Maintain the modular quest content library
- [x] Keep quest content split into ordered modular fragments

### Content library
- [x] `0001_all_quests.py`
- [x] `0001_prison_break_chain.py`
- [x] `0002_mercenary_guild_quests.py`
- [x] `0003_lord_quests.py`
- [x] `0004_enemy_lord_quests.py`
- [x] `0005_army_quests.py`
- [x] `0006_lady_quests.py`
- [x] `0007_mayor_quests.py`
- [x] `0008_village_elder_quests.py`
- [x] `0009_story_and_meta_quests.py`
- [x] `0010_sample_campaign_quests.py`
- [x] `_order_quests.txt`

### Content organization
- [x] Quest fragments are grouped by quest family and theme
- [x] The order manifest exists for deterministic build ordering
- [-] Cross-fragment gameplay verification still needs a final pass

### Result
- [x] The quest content is modular rather than monolithic

### Audit note
- [x] The quest fragment library is present and ordered.
- [-] The fragments still need final play-validated consistency checks.
- [ ] The phase is not fully done until the fragment set is verified in gameplay.

---

## Phase 11 — Finish live integration and verification
- [ ] Live gameplay integration
- [x] Battle/map/mission hook wiring
- [ ] Quest acceptance/rejection flow verification
- [ ] Quest completion/failure flow verification
- [ ] Reward/consequence flow verification
- [x] Build/export verification
- [ ] End-to-end playthrough testing
- [x] Final documentation cleanup

### Audit note
- [x] The source stack is wired and the quest journal contract tests have passed.
- [-] Live gameplay verification is still open because it depends on engine-level playtesting.
- [ ] The remaining phase items are still open until verified in actual gameplay contexts.
