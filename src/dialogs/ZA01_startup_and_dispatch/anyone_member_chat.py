DIALOGS = [
[anyone , "member_chat", [(store_conversation_troop, "$g_talk_troop"),
                           (try_begin),
                               (is_between, "$g_talk_troop", companions_begin, companions_end),
                               (talk_info_show, 1),
                               (call_script, "script_setup_talk_info_companions"),
                           (try_end),
                           (troop_get_type, reg65, "$g_talk_troop"),
							
                     (troop_get_type, reg65, "$g_talk_troop"),
                     (try_begin),
                       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                       (str_store_string, s64, "@{reg65?my Lady:my Lord}"), #bug fix
                       (str_store_string, s65, "@{reg65?my Lady:my Lord}"),
                       (str_store_string, s66, "@{reg65?My Lady:My Lord}"),
                     (else_try),
                       (str_store_string, s64, "@{reg65?madame:sir}"), #bug fix
                       (str_store_string, s65, "@{reg65?madame:sir}"),
                       (str_store_string, s66, "@{reg65?Madame:Sir}"),
                     (try_end),

                     (eq, 1, 0)],
   "Warning: This line is never displayed. It is just for storing conversation variables.", "close_window", []],
]
