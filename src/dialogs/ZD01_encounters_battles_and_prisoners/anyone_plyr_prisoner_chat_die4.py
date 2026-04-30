DIALOGS = [
[anyone|plyr, "prisoner_chat_die4", [], "(The prisoner struggles against his shackles, desperate to free himself and escape you, but to no avail. You slit their throat with a knife and watch, satisfied, as his corpse sags to the floor.)", "close_window",
   [(remove_troops_from_prisoners, "$g_talk_troop", 1),
    (call_script, "script_change_player_honor", -1)]],
]
