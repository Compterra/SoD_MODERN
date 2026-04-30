DIALOGS = [
[anyone|plyr, "companion_recruit_intro_response", [
                     (troop_get_slot, ":intro_response", "$g_talk_troop", slot_troop_intro_response_1),
                     (str_store_string, 6, ":intro_response")
      ], "{s6}", "companion_recruit_backstory_a", []],
]
