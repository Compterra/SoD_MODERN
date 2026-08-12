from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "companion_recruit_signup",
     [(is_between, "$g_talk_troop", companions_begin, companions_end),
      (troop_get_slot, ":signup", "$g_talk_troop", slot_troop_signup),
      (str_store_string, s68, ":signup"),
      (str_store_party_name, s20, "$g_encountered_party"),
      ],
     "{s68}", "companion_recruit_signup_b", []],
]
