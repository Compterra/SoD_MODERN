DIALOGS = [
[anyone, "village_elder_deliver_cattle_mission_accept", [], "Then we will keep the pens ready and the children from counting promises. Bring the cattle through safely, {sir/madam}; a village hears hooves before hope.", "close_window",
   [(assign, "$g_leave_encounter", 1),
    (call_script, "script_change_player_relation_with_center", "$current_town", 3),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],
]
