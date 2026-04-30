DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, 0),
                     (troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, pp_history_dismissed),
                     (troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
                     (str_store_string, 21, ":honorific"),
                     (troop_get_slot, ":speech", "$g_talk_troop", slot_troop_backstory_delayed),
                     (str_store_string, 5, ":speech"),
   ],
   "It is good to see you, {s21}! To tell you the truth, I had hoped to run into you.",
   "companion_was_dismissed", [
                     (troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_indeterminate),
      ]],
]
