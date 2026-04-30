DIALOGS = [
[anyone|plyr, "companion_recruit_backstory_response", [
                     (troop_get_slot, ":backstory_response", "$g_talk_troop", slot_troop_backstory_response_2),
                     (str_store_string, 7, ":backstory_response")
      ],  "{s7}", "close_window", [
          ]],
]
