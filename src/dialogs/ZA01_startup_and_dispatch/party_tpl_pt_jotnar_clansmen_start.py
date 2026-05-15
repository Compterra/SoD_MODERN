DIALOGS = [
[party_tpl|pt_jotnar_clansmen, "start", [
                                           (check_quest_active, "qst_jotnar_clan_free_clansmen"),
                                           (neg|check_quest_concluded, "qst_jotnar_clan_free_clansmen"),
                                           (quest_get_slot, ":quest_target_party", "qst_jotnar_clan_free_clansmen", slot_quest_target_party),
                                           (eq, "$g_encountered_party", ":quest_target_party"),
                                           (party_is_active, "$g_encountered_party"),
                                           (store_distance_to_party_from_party, ":dist", "$g_encountered_party", "p_sod_merc_guild_4"),
                                           (lt, ":dist", 2),
                                           ],
   "The base is close now. We can cover the last stretch ourselves.\
 You have our thanks, and every chain left behind will remember your name.", "close_window", [
                                                       (quest_get_slot, ":quest_target_party", "qst_jotnar_clan_free_clansmen", slot_quest_target_party),
                                                       (call_script, "script_succeed_quest", "qst_jotnar_clan_free_clansmen"),
                                                       (call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_jotnar_support, 2),
                                                       (call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_free_captives, 1),
                                                       (call_script, "script_change_troop_renown", "trp_player", 2),
                                                       (try_begin),
                                                         (gt, ":quest_target_party", 0),
                                                         (neq, ":quest_target_party", "p_main_party"),
                                                         (party_is_active, ":quest_target_party"),
                                                         (party_get_template_id, ":encounter_template", ":quest_target_party"),
                                                         (eq, ":encounter_template", "pt_jotnar_clansmen"),
													     (remove_party, ":quest_target_party"), #twan456
                                                       (try_end),
                                                       (assign, "$g_leave_encounter", 1),
                                                       ]],
]
