DIALOGS = [
[anyone , "start", [(store_conversation_troop, "$g_talk_troop"),
                     (store_conversation_agent, "$g_talk_agent"),
                     (store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),
                     (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
                     (assign, "$g_talk_troop_relation", reg0),

                     (try_begin),
                       (this_or_next|is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
                       (is_between, "$g_talk_troop", mayors_begin, mayors_end),
                       (party_get_slot, "$g_talk_troop_relation", "$current_town", slot_center_player_relation),
                     (try_end),
                     (store_relation, "$g_talk_troop_faction_relation", "$g_talk_troop_faction", "fac_player_faction"),

                     (assign, "$g_talk_troop_party", "$g_encountered_party"),
                     (try_begin),
                       (troop_slot_ge, "$g_talk_troop", slot_troop_leaded_party, 1),
                       (troop_get_slot, "$g_talk_troop_party", "$g_talk_troop", slot_troop_leaded_party),
                     (try_end),


                     (store_current_hours, "$g_current_hours"),
                     (troop_get_slot, "$g_talk_troop_last_talk_time", "$g_talk_troop", slot_troop_last_talk_time),
                     (troop_set_slot, "$g_talk_troop", slot_troop_last_talk_time, "$g_current_hours"),
                     (store_sub, "$g_time_since_last_talk", "$g_current_hours", "$g_talk_troop_last_talk_time"),
                     (troop_get_slot, "$g_talk_troop_met", "$g_talk_troop", slot_troop_met),
                     (troop_set_slot, "$g_talk_troop", slot_troop_met, 1),

                     (try_begin),
                       (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
                       (assign, "$g_enemy_strength", reg0),
                       (call_script, "script_party_calculate_strength", "p_main_party", 0),
                       (assign, "$g_ally_strength", reg0),
                       (try_begin),
                       (gt, "$g_enemy_strength", 0),
                       (store_mul, "$g_strength_ratio", "$g_ally_strength", 100),
                       (val_div, "$g_strength_ratio", "$g_enemy_strength"),
                       (else_try),
                       (assign, "$g_strength_ratio", 1000),
                       (try_end),
                     (try_end),

                     (assign, "$g_comment_found", 0),

                     (try_begin),
                       (troop_is_hero, "$g_talk_troop"),
                       (talk_info_show, 1),
                       (call_script, "script_setup_talk_info"),
                     (try_end),

                     (try_begin),
                       (is_between, "$g_talk_troop", kingdom_heroes_begin, kingdom_heroes_end),
                       (call_script, "script_get_relevant_comment_to_s42"),
                       (assign, "$g_comment_found", reg0),
                     (try_end),

                     (troop_get_type, reg65, "$g_talk_troop"),
                     (try_begin),
                       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                       (str_store_string, s64, "@{reg65?my Lady:my Lord}"), #bug fix
                       (str_store_string, s65, "@{reg65?my Lady:my Lord}"),
                       (str_store_string, s66, "@{reg65?My Lady:My Lord}"),
                       (str_store_string, s67, "@{reg65?My Lady:My Lord}"), #bug fix
                     (else_try),
                       (str_store_string, s64, "@{reg65?madame:sir}"), #bug fix
                       (str_store_string, s65, "@{reg65?madame:sir}"),
                       (str_store_string, s66, "@{reg65?Madame:Sir}"),
                       (str_store_string, s67, "@{reg65?Madame:Sir}"), #bug fix
                     (try_end),

                     (eq, 1, 0)],
   "Warning: This line is never displayed. It is just for storing conversation variables.", "close_window", []],
]
