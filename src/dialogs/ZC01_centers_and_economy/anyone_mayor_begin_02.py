DIALOGS = [
[anyone, "mayor_begin", [(check_quest_active, "qst_deal_with_night_bandits"),
                          (quest_slot_eq, "qst_deal_with_night_bandits", slot_quest_giver_troop, "$g_talk_troop"),
                          (check_quest_succeeded, "qst_deal_with_night_bandits"),
                         ],
   "Very nice work, {playername}, you made short work of those lawless curs.\
 Thank you kindly for all your help, and please accept this bounty of 150 denars.", "lord_deal_with_night_bandits_completed",
   [
     (add_xp_as_reward, 200),
     (call_script, "script_troop_add_gold", "trp_player", 150),
     (call_script, "script_change_player_relation_with_center", "$current_town", 1),
     (call_script, "script_end_quest", "qst_deal_with_night_bandits"),
    ]],
]
