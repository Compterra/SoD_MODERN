DIALOGS = [
[anyone, "lord_ask_leave_service_3", [], "As you wish. I hereby declare your oaths to be null and void.\
 You will no longer hold land or titles in my name, and you are released from your duties to my house.\
 You are free, {playername}.", "lord_ask_leave_service_end",
   [
        (call_script, "script_add_log_entry", logent_renounced_allegiance,   "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction"),
        (call_script, "script_player_leave_faction", 1),
    ]],
]
