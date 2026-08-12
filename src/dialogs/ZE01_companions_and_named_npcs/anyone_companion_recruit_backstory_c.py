from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "companion_recruit_backstory_c",
     [(is_between, "$g_talk_troop", companions_begin, companions_end),
      (troop_get_slot, ":backstory_c", "$g_talk_troop", slot_troop_backstory_c),
      (str_store_string, s68, ":backstory_c"),
      ],
     "{s68}", "companion_recruit_backstory_response", []],
]
