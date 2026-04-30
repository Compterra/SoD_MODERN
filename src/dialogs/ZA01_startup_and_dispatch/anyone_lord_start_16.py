DIALOGS = [
[anyone, "lord_start", [(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                         (store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_follow_spy"),
                         (eq, "$qst_follow_spy_no_active_parties", 1),
                         (party_count_prisoners_of_type, ":num_spies", "p_main_party", "trp_spy"),
                         (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", "trp_spy_partner"),
                         (eq, ":num_spies", 0),
                         (gt, ":num_spy_partners", 0),
                         ],
   "I asked you for two prisoners, {playername}, not one. Two. Still, I suppose you did capture the spy's handler,\
 the more important one of the pair. The spy will not dare return here and will prove quite useless to\
 whatever master he served. 'Tis better than nothing.\
 However, you'll understand if I pay you half the promised reward for what is but half a success.", "lord_follow_spy_half_completed",
   [(party_remove_prisoners, "p_main_party", "trp_spy_partner", 1),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
    (call_script, "script_troop_add_gold", "trp_player", 1000),
    (add_xp_as_reward, 400),
    (call_script, "script_end_quest", "qst_follow_spy")]],
]
