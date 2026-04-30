DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_talk_troop_relation", -5),
                    ],
   "Good to see you here, {playername}. {s43}", "close_window", [
                    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_default"),
       ]],
]
