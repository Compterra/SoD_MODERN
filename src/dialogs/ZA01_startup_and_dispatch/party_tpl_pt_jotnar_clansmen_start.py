DIALOGS = [
[party_tpl|pt_jotnar_clansmen, "start", [
                                           (store_distance_to_party_from_party, ":dist", "p_main_party", "p_sod_merc_guild_4"),
                                           (lt, ":dist", 2),
                                           ],
   "The base is close now. We can cover the last stretch ourselves.\
 You have our thanks, and every chain left behind will remember your name.", "close_window", [
                                                       (call_script, "script_succeed_quest", "qst_jotnar_clan_free_clansmen"),
                                                       (call_script, "script_change_troop_renown", "trp_player", 2),
                                                       (try_begin),
                                                         (gt, "$g_encountered_party", 0),
                                                         (neq, "$g_encountered_party", "p_main_party"),
                                                         (party_is_active, "$g_encountered_party"),
                                                         (party_get_template_id, ":encounter_template", "$g_encountered_party"),
                                                         (eq, ":encounter_template", "pt_jotnar_clansmen"),
													     (remove_party, "$g_encountered_party"), #twan456
                                                       (try_end),
                                                       (assign, "$g_leave_encounter", 1),
                                                       ]],
]
