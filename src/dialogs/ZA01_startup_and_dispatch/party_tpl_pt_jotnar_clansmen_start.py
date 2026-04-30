DIALOGS = [
[party_tpl|pt_jotnar_clansmen, "start", [
                                           (store_distance_to_party_from_party, ":dist", "p_main_party", "p_sod_merc_guild_4"),
                                           (lt, ":dist", 2),
                                           ],
   "Well, we have almost reached the base. We can cover the rest of the way ourselves.\
 Thanks for escorting us. Good luck.", "close_window", [
                                                       (call_script, "script_succeed_quest", "qst_jotnar_clan_free_clansmen"),
                                                       (call_script, "script_change_troop_renown", "trp_player", 2),
													   (remove_party, "$g_encountered_party"), #twan456
                                                       (assign, "$g_leave_encounter", 1),
                                                       ]],
]
