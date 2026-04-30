DIALOGS = [
[anyone|plyr, "companion_recruit_signup_response", [
                    (hero_can_join, "p_main_party"),
                     (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_2),
                     (str_store_string, 7, ":signup_response")
      ],  "{s7}", "close_window", [
          ]],
]
