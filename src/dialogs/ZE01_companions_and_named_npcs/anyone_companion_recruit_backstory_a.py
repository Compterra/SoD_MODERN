from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "companion_recruit_backstory_a",
     [(troop_get_slot, ":backstory_a", "$g_talk_troop", slot_troop_backstory_a),
      (str_store_string, 5, ":backstory_a"),
      (str_store_string, 19, "str_here_plus_space"),
      (str_store_party_name, 20, "$g_encountered_party"),
      ],
     "{s5}", "companion_recruit_backstory_b", []],
]
