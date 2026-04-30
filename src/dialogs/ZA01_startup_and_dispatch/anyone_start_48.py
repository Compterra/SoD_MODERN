DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_turned_down_twice, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_quit),
                     (troop_get_slot, ":speech", "$g_talk_troop", slot_troop_rehire_speech),
                     (str_store_string, 5, ":speech"),
   ],
   "{s5}", "companion_rehire", [
                     (troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate),
      ]],
]
