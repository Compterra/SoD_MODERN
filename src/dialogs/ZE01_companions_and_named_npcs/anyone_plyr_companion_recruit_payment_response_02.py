DIALOGS = [
[anyone|plyr, "companion_recruit_payment_response", [
                     (is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_2),
                     (str_store_string, s69, ":signup_response")
      ],  "Your price is beyond my purse today.", "close_window", [
          ]],
]
