from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "companion_recruit_backstory_b",
     [(is_between, "$g_talk_troop", companions_begin, companions_end),
      (troop_get_slot, ":backstory_b", "$g_talk_troop", slot_troop_backstory_b),
      (str_store_string, s68, ":backstory_b"),
      (str_store_party_name, s20, "$g_encountered_party"),
      ],
     "{s68}", "companion_recruit_backstory_c", []],
]
