DIALOGS = [
[anyone, "start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_slavers_bring_back_runaway_slaves"),
						 (quest_slot_eq, ":lords_quest", slot_quest_giver_center, "$g_encountered_party"),
                         (check_quest_succeeded, "qst_slavers_bring_back_runaway_slaves")],
   "Damn me, but you've done it, {playername}. All the slaves are back.\
 You certainly earned your reward. Here, take it, with my compliments.", "gm_pretalk",
   [(call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 4),
    (call_script, "script_troop_add_gold", "trp_player", 300),
    (add_xp_as_reward, 300),
    (call_script, "script_succeed_quest", "qst_slavers_bring_back_runaway_slaves"),
    (call_script, "script_end_quest", "qst_slavers_bring_back_runaway_slaves"),
    ]],
]
