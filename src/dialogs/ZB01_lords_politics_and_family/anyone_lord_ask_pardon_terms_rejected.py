DIALOGS = [
[anyone, "lord_ask_pardon_terms_rejected",
   [], "Then get out of my sight, traitor! Begone with you, and do not come back!", "close_window",
   [
     (assign, "$g_leave_encounter", 1),
     #TODO: Add relation drop. $players_oath_renounced_begin_time can also be reset to current time for worse conditions in the next conversation.
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -5),
     ]],
]
