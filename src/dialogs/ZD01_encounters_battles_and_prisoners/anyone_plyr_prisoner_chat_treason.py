DIALOGS = [
[anyone|plyr, "prisoner_chat_treason", [(call_script, "script_store_troop_name", s1, "$g_talk_troop"), (str_store_faction_name, s2, "$players_kingdom")],
    "{s1}, you have committed cimes against the {s2}, for which you will now stand trial.^How plead you?", "prisoner_chat_treason_plead",
    [
      # determine the noble's reaction to this accusation
      (store_random_in_range, reg0, 0, 100),
      (val_mod, reg0, 4),
      #TODO: weight the reaction according to the renown?  Or at least according to king or not...
      (troop_set_slot, "$g_talk_troop", slot_prisoner_agreed, reg0),
    ]
  ],
]
