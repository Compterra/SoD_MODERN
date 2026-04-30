DIALOGS = [
[anyone, "lord_mission_raise_troops_accepted", [], "You've taken a weight off my shoulders, {playername}.\
 I shall tell my sergeants to send you the recruits and attach them to your command.\
 Also, I'll advance you some money to help with expenses. Here, this purse should do it.\
 Thank you for your help.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_troop_add_gold", "trp_player", 100),
    (quest_get_slot, ":recruit_troop", "$random_quest_no", slot_quest_object_troop),
    (quest_get_slot, ":num_recruits", "$random_quest_no", slot_quest_target_amount),
    (party_add_members, "p_main_party", ":recruit_troop", ":num_recruits"),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
    (assign, "$g_leave_encounter", 1),
   ]],
]
