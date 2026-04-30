SIMPLE_TRIGGERS = [
(72, [(gt, "$g_force_peace_faction_1", 0),
        (gt, "$g_force_peace_faction_2", 0),
        (try_begin),
          (store_relation, ":relation", "$g_force_peace_faction_1", "$g_force_peace_faction_2"),
          (lt, ":relation", 0),
          (call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_force_peace_faction_1", "$g_force_peace_faction_2", 1),
        (try_end),
        (assign, "$g_force_peace_faction_1", 0),
        (assign, "$g_force_peace_faction_2", 0),
       ]),
]
