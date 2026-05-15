from header_dialogs import *
from module_constants import *

DIALOGS = [
    [plyr, "companion_personalityclash_response", [], "Drop it. Your temper is not command.", "close_window", [
        (call_script, "script_sod_companion_shift_approval", "$map_talk_troop", -2),
        (assign, "$npc_with_personality_clash", 0),
        (assign, "$npc_map_talk_context", 0),
    ]],
]
