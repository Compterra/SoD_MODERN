DIALOGS = [
[anyone|plyr, "companion_recruit_backstory_response", [
                     (troop_get_slot, ":backstory_response", "$g_talk_troop", slot_troop_backstory_response_1),
                     (str_store_string, 6, ":backstory_response")
      ], "{s6}", "companion_recruit_signup", []],
]
