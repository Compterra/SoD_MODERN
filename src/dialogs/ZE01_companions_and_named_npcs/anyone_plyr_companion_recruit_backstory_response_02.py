DIALOGS = [
[anyone|plyr, "companion_recruit_backstory_response", [
                     (is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_get_slot, ":backstory_response", "$g_talk_troop", slot_troop_backstory_response_2),
                     (str_store_string, s69, ":backstory_response")
      ],  "{s69}", "close_window", [
          ]],
]
