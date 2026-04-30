DIALOGS = [
[anyone, "lord_start", [(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                         (store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_follow_spy"),
                         (eq, "$qst_follow_spy_no_active_parties", 1),
                         (party_count_prisoners_of_type, ":num_spies", "p_main_party", "trp_spy"),
                         (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", "trp_spy_partner"),
                         (gt, ":num_spies", 0),
                         (eq, ":num_spy_partners", 0), ],
   "{s1}", "lord_follow_spy_half_completed",
   [(call_script, "script_sod_quest_dialogue_describe_reaction", "$g_talk_troop"),
    (call_script, "script_sod_quest_dialogue_describe_stage", "$g_talk_troop"),
    (str_store_string, s1, "@Blast and damn you! I wanted TWO prisoners, {playername} -- what you've brought me is one step short of\
 useless! I already know everything the spy knows, it was the handler I was after.\
 Here, half a job gets you half a reward. Take it and begone.^{s4}"),
    (party_remove_prisoners, "p_main_party", "trp_spy", 1),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (call_script, "script_troop_add_gold", "trp_player", 1000),
    (add_xp_as_reward, 400),
    (call_script, "script_end_quest", "qst_follow_spy")]],
]
