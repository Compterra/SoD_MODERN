DIALOGS = [
[anyone|plyr, "prisoner_chat_treason", [(call_script, "script_store_troop_name", s1, "$g_talk_troop"), (str_store_faction_name, s2, "$players_kingdom")],
    "{s1}, you have committed crimes against the {s2}, for which you will now stand trial.^How plead you?", "prisoner_chat_treason_plead",
    [
      (call_script, "script_sod_treason_select_plea_reaction", "$g_talk_troop"),
    ]
  ],
]
