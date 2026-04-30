DIALOGS = [
[anyone, "town_dweller_poor_paid", [], "{My lord/My good lady}. \
 You are so good and generous. I will tell everyone how you helped us.", "close_window",
   [(call_script, "script_change_player_relation_with_center", "$g_encountered_party", 1),
    (call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
    (assign, ":walker_no", reg2),
    (call_script, "script_center_set_walker_to_type", "$g_encountered_party", ":walker_no", walkert_needs_money_helped),
    ]],
]
