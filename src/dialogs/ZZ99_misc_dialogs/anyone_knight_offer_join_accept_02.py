DIALOGS = [
[anyone , "knight_offer_join_accept", [], "Ah, certainly, it might be fun!", "close_window", [
      (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
      (assign, "$g_leave_encounter", 1)
      ]],
]
