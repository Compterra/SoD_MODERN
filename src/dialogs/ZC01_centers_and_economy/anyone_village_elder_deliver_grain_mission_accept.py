DIALOGS = [
[anyone, "village_elder_deliver_grain_mission_accept", [], "Then we will wait with empty bins and careful hope. Bring the grain through, {sir/madam}; every sack arrives as supper, seed, and one less argument at the hearth.", "close_window",
   [(assign, "$g_leave_encounter", 1),
    (call_script, "script_change_player_relation_with_center", "$current_town", 5),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],
]
