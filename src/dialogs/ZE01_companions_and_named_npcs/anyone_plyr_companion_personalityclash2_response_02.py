from header_dialogs import *
from module_constants import *

DIALOGS = [
    [plyr, "companion_personalityclash2_response", [], "Stay, but do not swallow it. Say what needs saying.", "close_window", [
        (call_script, "script_sod_companion_shift_approval", "$map_talk_troop", 3),
        (troop_set_slot, "$map_talk_troop", slot_troop_personalityclash2_state, 1),
        (assign, "$npc_with_personality_clash_2", 0),
        (assign, "$npc_map_talk_context", 0),
    ]],
]
