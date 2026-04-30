DIALOGS = [
[anyone, "village_elder_deliver_grain_mission_accept", [], "Thank you, {sir/madam}. We'll be praying for you night and day.", "close_window",
   [(assign, "$g_leave_encounter", 1),
    (call_script, "script_change_player_relation_with_center", "$current_town", 5),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],
]
