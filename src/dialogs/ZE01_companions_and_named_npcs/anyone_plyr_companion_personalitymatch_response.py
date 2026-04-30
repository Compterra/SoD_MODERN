from header_dialogs import *
from header_operations import *
from module_constants import *

DIALOGS = [
    [anyone|plyr, "companion_personalitymatch_response", [], "You are right. We do not have to agree on everything to travel well together. I will remember that the next time the road makes us both tired and short-tempered.", "close_window", [(troop_set_slot, "$g_talk_troop", slot_troop_personalitymatch_state, 1)]],
]