from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "companion_recruit_backstory_a",
     [(is_between, "$g_talk_troop", companions_begin, companions_end),
      (troop_get_slot, ":backstory_a", "$g_talk_troop", slot_troop_backstory_a),
      (str_store_string, s68, ":backstory_a"),
      (str_store_string, s19, "str_here_plus_space"),
      (str_store_party_name, s20, "$g_encountered_party"),
      ],
     "{s68}", "companion_recruit_backstory_b", []],
]
