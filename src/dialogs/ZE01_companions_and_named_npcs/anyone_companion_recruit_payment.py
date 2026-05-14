from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "companion_recruit_payment",
     [(store_sub, ":npc_offset", "$g_talk_troop", "trp_npc1"),
      (store_add, ":dialog_line", "str_npc1_payment", ":npc_offset"),
      (str_store_string, s5, ":dialog_line"),
      (troop_get_slot, reg3, "$g_talk_troop", slot_troop_payment_request),
      (str_store_party_name, s20, "$g_encountered_party"),
      ],
     "{s5}", "companion_recruit_payment_response", []],
]
