from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "companion_recruit_backstory_c",
     [(troop_get_slot, ":backstory_c", "$g_talk_troop", slot_troop_backstory_c),
      (str_store_string, 5, ":backstory_c"),
      ],
     "{s5}", "companion_recruit_backstory_response", []],
]
