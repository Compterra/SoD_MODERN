# Phase 4 event-driven quest API

Phase 4 adds a canonical world-event catalog for quest progression and a small source-adapter facade for game systems that emit events.

## Canonical world events

Use `src.quests.quest_events.quest_world_event_names()` to read the stable Phase 4 event set:

- `battle_started`
- `battle_ended`
- `agent_killed`
- `prisoner_captured`
- `prisoner_freed`
- `party_entered_center`
- `conversation_started`
- `conversation_ended`
- `item_acquired`
- `item_lost`
- `relation_changed`
- `faction_state_changed`
- `village_raided`
- `center_besieged`
- `mission_succeeded`
- `mission_failed`
- `caravan_created`
- `caravan_destroyed`
- `time_passed`
- `inventory_updated`

`src.quests.quest_events.quest_world_event_factories()` returns the matching per-event factory map, and each factory returns a `QuestWorldEvent`.

## Source-adapter helpers

`src.quests.quest_event_sources` provides a compact emission facade:

- `emit_world_event(...)`
- `emit_battle_started(...)`
- `emit_battle_ended(...)`
- `emit_agent_killed(...)`
- `emit_prisoner_captured(...)`
- `emit_prisoner_freed(...)`
- `emit_party_entered_center(...)`
- `emit_conversation_started(...)`
- `emit_conversation_ended(...)`
- `emit_item_acquired(...)`
- `emit_item_lost(...)`
- `emit_relation_changed(...)`
- `emit_faction_state_changed(...)`
- `emit_village_raided(...)`
- `emit_center_besieged(...)`
- `emit_mission_succeeded(...)`
- `emit_mission_failed(...)`
- `emit_caravan_created(...)`
- `emit_caravan_destroyed(...)`
- `emit_time_passed(...)`
- `emit_inventory_updated(...)`

If no runtime, journal, or dispatcher target is supplied, the helpers return a `QuestWorldEvent`. Event names are canonical lower snake_case values, and the runtime matcher accepts the same event names through subscription specs.

## Subscription keys

Quest event subscriptions continue to use the stable spec keys:

`event_types`, `quest_ids`, `stage_ids`, `faction_ids`, `troop_ids`, `center_ids`, `party_ids`, `region_ids`, `location_ids`, `sources`, `categories`, `tags`, `payload_keys`, `priority`, `enabled`, `once`, `terminal_only`, `non_terminal_only`, `metadata`, and `callback`.