DIALOGS = [
[anyone|plyr, "companion_recruit_payment_response", [
                     (troop_get_slot, ":signup_response", "$g_talk_troop", slot_troop_signup_response_2),
                     (str_store_string, s7, ":signup_response")
      ],  "Sorry. I can't afford that at the moment.", "close_window", [
          ]],
]
