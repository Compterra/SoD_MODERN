DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_bring_back_runaway_serfs"),
                         (check_quest_concluded, "qst_bring_back_runaway_serfs"),
                         (assign, reg17, "$qst_bring_back_runaway_serfs_num_parties_returned")],
   "You disappoint me, {playername}. There were 3 groups of serfs that I charged you to return. 3. Not {reg17}.\
 I suppose the ones who did come back shall have to work twice as hard to make up for those that got away.\
 As for your reward, {playername}, I'll only pay you for the serfs you returned, not the ones you let fly.\
 Here. Take it, and let this business be done.", "lord_runaway_serf_half_completed",
   [(store_mul, ":reward", "$qst_bring_back_runaway_serfs_num_parties_returned", 100),
    (val_div, ":reward", 2),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", "$qst_bring_back_runaway_serfs_num_parties_returned"),
    (call_script, "script_troop_add_gold", "trp_player", ":reward"),
    (add_xp_as_reward, ":reward"),


    (call_script, "script_objectionable_action", tmt_humanitarian, "str_round_up_serfs"),

    (call_script, "script_end_quest", "qst_bring_back_runaway_serfs"),
    ]],
]
