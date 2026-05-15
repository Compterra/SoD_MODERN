DIALOGS = [
[anyone|plyr, "prisoner_chat_treason_guilty", [], "For your many crimes against {s1}, I hereby sentence you to death, to be carried out immediately.  Have you any final words to say?", "prisoner_chat_treason_final_words",
    [
      (call_script, "script_sod_treason_select_final_words", "$g_talk_troop"),
    ]
  ],
]
