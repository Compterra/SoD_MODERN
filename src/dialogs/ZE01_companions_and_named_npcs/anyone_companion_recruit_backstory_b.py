from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "companion_recruit_backstory_b",
     [(troop_get_slot, ":backstory_b", "$g_talk_troop", slot_troop_backstory_b),
      (str_store_string, 5, ":backstory_b"),
      (str_store_party_name, 20, "$g_encountered_party"),
      ],
     "{s5}", "companion_recruit_backstory_c", []],
]
