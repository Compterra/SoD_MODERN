from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "event_triggered", [
        (eq, "$npc_map_talk_context", slot_troop_personalitymatch_state),
        (store_conversation_troop, "$map_talk_troop"),
        (eq, "$map_talk_troop", "$npc_with_personality_match"),
        (main_party_has_troop, "$map_talk_troop"),
        (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalitymatch_object),
        (main_party_has_troop, ":object"),
    ], "You and I do not always agree, but you take blame and leave room for other voices. That matters.", "companion_personalitymatch_response", [
        (assign, "$npc_with_personality_match", 0),
    ]],
]
