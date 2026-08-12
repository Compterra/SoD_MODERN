from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "companion_recruit_backstory_delayed",
     [(is_between, "$g_talk_troop", companions_begin, companions_end),
      (troop_get_slot, ":backstory_delayed", "$g_talk_troop", slot_troop_backstory_delayed),
      (str_store_string, s68, ":backstory_delayed"),
      ],
     "{s68}", "companion_recruit_backstory_delayed_response", []],
]
