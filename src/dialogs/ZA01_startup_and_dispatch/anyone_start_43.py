DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (eq, "$g_talk_troop_met", 0),
                     (troop_get_slot, ":intro", "$g_talk_troop", slot_troop_intro),
                     (str_store_string, 5, ":intro"),
                     (str_store_party_name, 20, "$g_encountered_party"),
   ],
   "{s5}", "companion_recruit_intro_response", [
                    (troop_set_slot, "$g_talk_troop", slot_troop_first_encountered, "$g_encountered_party"),
       ]],
]
