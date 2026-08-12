DIALOGS = [
[anyone|plyr, "companion_recruit_signup_response", [
                    (is_between, "$g_talk_troop", companions_begin, companions_end),
                    (hero_can_join, "p_main_party"),
                    (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_2),
                    (str_store_string, s69, ":signup_response")
      ],  "{s69}", "close_window", [
          ]],
]
