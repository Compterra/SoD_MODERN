DIALOGS = [
[anyone|plyr, "companion_recruit_intro_response", [
                     (troop_get_slot, ":intro_response", "$g_talk_troop", slot_troop_intro_response_2),
                     (str_store_string, 7, ":intro_response")
      ],  "{s7}", "close_window", [
          ]],
]
