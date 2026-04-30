DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_follow_spy"),
                         (eq, "$qst_follow_spy_no_active_parties", 1),
                         (party_count_prisoners_of_type, ":num_spies", "p_main_party", "trp_spy"),
                         (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", "trp_spy_partner"),
                         (eq, ":num_spies", 0),
                         (eq, ":num_spy_partners", 0),
                         ],
   "Truly, {playername}, you are nothing short of totally incompetent.\
 Failing to capture both the spy AND his handler plumbs astonishing new depths of failure.\
 Forget any reward I offered you. You've done nothing to earn it.", "lord_follow_spy_failed",
   [
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -2),
    (call_script, "script_end_quest", "qst_follow_spy"),
    ]],
]
