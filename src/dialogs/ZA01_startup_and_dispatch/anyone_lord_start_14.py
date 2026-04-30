DIALOGS = [
[anyone, "lord_start", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
             (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                         (store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_follow_spy"),
                         (eq, "$qst_follow_spy_no_active_parties", 1),
                         (party_count_prisoners_of_type, ":num_spies", "p_main_party", "trp_spy"),
                         (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", "trp_spy_partner"),
                         (gt, ":num_spies", 0),
                         (gt, ":num_spy_partners", 0)],
   "{s1}", "lord_follow_spy_completed",
   [(call_script, "script_sod_quest_dialogue_describe_reaction", "$g_talk_troop"),
    (call_script, "script_sod_quest_dialogue_describe_stage", "$g_talk_troop"),
    (str_store_string, s1, "@Beautiful work, {playername}! You captured both the spy and his handler, just as I'd hoped,\
 and the pair are now safely ensconced in my dungeon, waiting to be questioned.\
 My torturer shall be busy tonight! Anyway, I'm very pleased with your success, {playername}, and I give you\
 this purse as a token of my appreciation.^{s4}"),
    (party_remove_prisoners, "p_main_party", "trp_spy", 1),
    (party_remove_prisoners, "p_main_party", "trp_spy_partner", 1),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 4),
    (call_script, "script_troop_add_gold", "trp_player", 2000),
    (add_xp_as_reward, 4000),
    (call_script, "script_end_quest", "qst_follow_spy")]],
]
