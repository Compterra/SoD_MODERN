DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    ],
   "{s43}", "close_window", [
                    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_unfriendly_default"),
                    ]],
]
