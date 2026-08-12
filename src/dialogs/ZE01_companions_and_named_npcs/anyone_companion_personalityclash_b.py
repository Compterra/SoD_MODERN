from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "event_triggered", [
        (eq, "$npc_map_talk_context", slot_troop_personalityclash_state),
        (store_conversation_troop, "$map_talk_troop"),
        (eq, "$map_talk_troop", "$npc_with_personality_clash"),
        (is_between, "$map_talk_troop", companions_begin, companions_end),
        (main_party_has_troop, "$map_talk_troop"),
        (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash_object),
        (is_between, ":object", companions_begin, companions_end),
        (main_party_has_troop, ":object"),
    ], "I have held my tongue long enough. This quarrel needs an answer before the camp inherits it.", "companion_personalityclash_response", [
        (assign, "$npc_with_personality_clash", 0),
    ]],
]
