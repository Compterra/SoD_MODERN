from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "companion_recruit_signup",
     [(troop_get_slot, ":signup", "$g_talk_troop", slot_troop_signup),
      (str_store_string, 5, ":signup"),
      (str_store_party_name, 20, "$g_encountered_party"),
      ],
     "{s5}", "companion_recruit_signup_b", []],
]
