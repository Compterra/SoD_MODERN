from header_dialogs import *
from header_operations import *
from module_constants import *

DIALOGS = [
    [anyone|plyr, "companion_personalitymatch_response", [], "Agreed. We can disagree and still keep the company whole.", "close_window", [
        (call_script, "script_sod_companion_shift_approval", "$g_talk_troop", 2),
        (troop_set_slot, "$g_talk_troop", slot_troop_personalitymatch_state, 1),
        (assign, "$npc_with_personality_match", 0),
        (assign, "$npc_map_talk_context", 0),
    ]],
]
