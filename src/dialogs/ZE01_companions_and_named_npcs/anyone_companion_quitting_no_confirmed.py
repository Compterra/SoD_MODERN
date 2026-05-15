from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "companion_quitting_no_confirmed", [], "Then I stay. Respect runs both ways.", "close_window", [
        (troop_get_slot, ":approval", "$g_talk_troop", slot_troop_companion_approval),
        (val_add, ":approval", 8),
        (val_clamp, ":approval", 0, 101),
        (troop_set_slot, "$g_talk_troop", slot_troop_companion_approval, ":approval"),
        (call_script, "script_sod_companion_get_approval_band_to_reg", "$g_talk_troop"),
        (troop_set_slot, "$g_talk_troop", slot_troop_companion_trust_tier, reg0),
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
