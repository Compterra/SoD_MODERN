DIALOGS = [
[anyone, "start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_slavers_bring_back_runaway_slaves"),
						 (quest_slot_eq, ":lords_quest", slot_quest_giver_center, "$g_encountered_party"),
                         (check_quest_concluded, "qst_slavers_bring_back_runaway_slaves"),
                         (assign, reg17, "$qst_bring_back_runaway_slaves_num_parties_returned")],
   "You disappoint me, {playername}. There were 3 groups of slaves that I charged you to return. 3. Not {reg17}.\
 I suppose the ones who did come back shall have to work twice as hard to make up for those that got away.\
 As for your reward, {playername}, I'll only pay you for the slaves you returned, not the ones you let fly.\
 Here. Take it, and let this business be done.", "gm_runaway_slave_half_completed",
   [(store_mul, ":reward", "$qst_bring_back_runaway_slaves_num_parties_returned", 100),
    (val_div, ":reward", 2),
    (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", "$qst_bring_back_runaway_slaves_num_parties_returned"),
    (call_script, "script_troop_add_gold", "trp_player", ":reward"),
    (add_xp_as_reward, ":reward"),
    (call_script, "script_succeed_quest", "qst_slavers_bring_back_runaway_slaves"),
    (call_script, "script_end_quest", "qst_slavers_bring_back_runaway_slaves"),
    ]],
]
