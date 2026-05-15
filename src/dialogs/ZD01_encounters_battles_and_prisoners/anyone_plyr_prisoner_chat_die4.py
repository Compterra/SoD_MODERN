DIALOGS = [
[anyone, "prisoner_chat_die4", [], "(The prisoner strains against the shackles, desperate to escape. You slit the prisoner's throat and watch the body sag to the floor.)", "close_window",
   [(remove_troops_from_prisoners, "$g_talk_troop", 1),
    (call_script, "script_change_player_honor", -1)]],
]
