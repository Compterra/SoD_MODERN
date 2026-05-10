from header_dialogs import *
from module_constants import *

DIALOGS = [
    [plyr, "companion_quitting_persuasion_02", [], "Then stay because the company is better with you in it, not because I would rather not lose the argument.", "close_window", [
        (troop_get_slot, ":approval", "$g_talk_troop", slot_troop_companion_approval),
        (val_add, ":approval", 12),
        (val_clamp, ":approval", 0, 101),
        (troop_set_slot, "$g_talk_troop", slot_troop_companion_approval, ":approval"),
        (try_begin),
          (ge, ":approval", 45),
          (troop_set_slot, "$g_talk_troop", slot_troop_companion_warning_state, sod_companion_warning_redeemed),
        (else_try),
          (troop_set_slot, "$g_talk_troop", slot_troop_companion_warning_state, sod_companion_warning_acknowledged),
        (try_end),
        (store_current_day, ":cur_day"),
        (troop_set_slot, "$g_talk_troop", slot_troop_companion_last_reaction_day, ":cur_day"),
    ]],
]
