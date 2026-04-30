DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_bring_back_runaway_serfs"),
                         (check_quest_succeeded, "qst_bring_back_runaway_serfs")],
   "Damn me, but you've done it, {playername}. All the serfs are back and they're busy preparing for the harvest.\
 You certainly earned your reward. Here, take it, with my compliments.", "lord_generic_mission_completed",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 4),
    (call_script, "script_troop_add_gold", "trp_player", 300),
    (add_xp_as_reward, 300),
    (call_script, "script_end_quest", "qst_bring_back_runaway_serfs"),
    (call_script, "script_objectionable_action", tmt_humanitarian, "str_round_up_serfs"),
    ]],
]
