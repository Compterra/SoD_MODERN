DIALOGS = [
[anyone, "lord_ask_pardon_terms_rejected",
   [], "Then get out of my sight, traitor! Begone with you, and do not come back!", "close_window",
   [
     (assign, "$g_leave_encounter", 1),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -5),
     (store_current_hours, "$players_oath_renounced_begin_time"),
     (assign, "$players_oath_renounced_given_center", 0),
     (assign, "$players_oath_renounced_terms_state", 0),
     ]],
]
