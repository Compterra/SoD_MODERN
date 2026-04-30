DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_scattered),
                     (assign, ":battle_fate", "str_battle_fate_1"),
                     (store_random_in_range, ":fate_roll", 0, 100),
                     (val_mod, ":fate_roll", 5),
                     (val_add, ":battle_fate", ":fate_roll"),
                     (str_store_string, 6, ":battle_fate"),
                     (troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
                     (str_store_string, 5, ":honorific"),
   ],
   "It is good to see you alive, {s5}! {s6}, and I did not know whether you had been captured, or slain, or got away. I've been roaming around since then, looking for you. Shall I get my gear together and rejoin your company?",
   "companion_rehire", [
                     (troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate),
      ]],
]
