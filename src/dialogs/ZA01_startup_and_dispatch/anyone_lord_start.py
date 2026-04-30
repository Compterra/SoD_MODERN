DIALOGS = [
[anyone, "lord_start", [(gt, "$g_comment_found", 0), #changed to s32 from s62 because overlaps with setup_talk_info strings
                        ],  "{s42}", "lord_start", [
                         (try_begin),
                           (neq, "$log_comment_relation_change", 0),
                           (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", "$log_comment_relation_change"),
                         (try_end),
                         (assign, "$g_comment_found", 0),
                         ]],
]
