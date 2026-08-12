DIALOGS = [
[anyone|plyr, "companion_recruit_intro_response", [
                     (is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_get_slot, ":intro_response", "$g_talk_troop", slot_troop_intro_response_1),
                     (str_store_string, s69, ":intro_response")
      ], "{s69}", "companion_recruit_backstory_a", []],
]
