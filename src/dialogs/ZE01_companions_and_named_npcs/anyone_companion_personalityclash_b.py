from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "event_triggered", [
        (eq, "$npc_map_talk_context", slot_troop_personalityclash_state),
        (store_conversation_troop, "$map_talk_troop"),
        (eq, "$map_talk_troop", "$npc_with_personality_clash"),
        (main_party_has_troop, "$map_talk_troop"),
        (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash_object),
        (main_party_has_troop, ":object"),
    ], "I have been patient, but patience is not the same as approval. If tempers keep scraping the same stone, we will warn the camp before a spark becomes a fire.", "companion_personalityclash_response", [
        (assign, "$npc_with_personality_clash", 0),
    ]],
]
