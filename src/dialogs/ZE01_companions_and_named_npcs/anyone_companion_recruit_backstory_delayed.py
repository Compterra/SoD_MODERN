from header_dialogs import *
from module_constants import *

DIALOGS = [
    [anyone, "companion_recruit_backstory_delayed",
     [(troop_get_slot, ":backstory_delayed", "$g_talk_troop", slot_troop_backstory_delayed),
      (str_store_string, 5, ":backstory_delayed"),
      ],
     "{s5}", "companion_recruit_backstory_delayed_response", []],
]
