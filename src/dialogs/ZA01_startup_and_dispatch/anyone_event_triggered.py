DIALOGS = [
[anyone , "event_triggered", [(store_conversation_troop, "$g_talk_troop"),
                           # The generic companion-reaction routes consume only
                           # the event pair recorded by companions_event_triggered.
                           # This preamble runs before every event_triggered route,
                           # so stale state is cleared before first-match selection.
                           (try_begin),
                               (eq, "$g_companion_event_active", 1),
                               (is_between, "$g_companion_event_actor_a", companions_begin, companions_end),
                               (is_between, "$g_companion_event_actor_b", companions_begin, companions_end),
                               (main_party_has_troop, "$g_companion_event_actor_a"),
                               (main_party_has_troop, "$g_companion_event_actor_b"),
                               (this_or_next|eq, "$g_talk_troop", "$g_companion_event_actor_a"),
                               (eq, "$g_talk_troop", "$g_companion_event_actor_b"),
                           (else_try),
                               (eq, "$g_companion_event_active", 1),
                               (assign, "$g_companion_event_active", 0),
                               (assign, "$g_companion_event_actor_a", -1),
                               (assign, "$g_companion_event_actor_b", -1),
                               (assign, "$g_companion_event_reaction_tier", -1),
                               (assign, "$g_companion_event_average_cohesion", -1),
                               (assign, "$g_companion_event_clash_severity", -1),
                               (assign, "$g_companion_event_reconciliation", -1),
                               (assign, "$g_companion_event_variant", -1),
                           (try_end),
                           (try_begin),
                               (is_between, "$g_talk_troop", companions_begin, companions_end),
                               (main_party_has_troop, "$g_talk_troop"),
                               (call_script, "script_setup_talk_info_companions"),
                           (try_end),

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
