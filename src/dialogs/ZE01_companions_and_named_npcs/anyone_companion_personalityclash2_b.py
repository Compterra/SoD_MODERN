from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "event_triggered", [
        (eq, "$npc_map_talk_context", slot_troop_personalityclash2_state),
        (store_conversation_troop, "$map_talk_troop"),
        (eq, "$map_talk_troop", "$npc_with_personality_clash_2"),
        (main_party_has_troop, "$map_talk_troop"),
        (troop_get_slot, ":object", "$map_talk_troop", slot_troop_personalityclash2_object),
        (main_party_has_troop, ":object"),
    ], "I have let this go too many times. If we travel together, we need more than silence and resentment.", "companion_personalityclash2_response", [
        (assign, "$npc_with_personality_clash_2", 0),
    ]],
]
