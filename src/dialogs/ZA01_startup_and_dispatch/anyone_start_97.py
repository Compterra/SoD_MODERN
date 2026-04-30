DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (ge, "$g_talk_troop_relation", 20),
                    (ge, "$g_relation_boost", 5),
                    ],
   "You arrived just in the nick of time! {playername}. You have my deepest thanks! {s43}", "close_window", [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_battle_won_default"),
       (try_begin),
         (party_stack_get_troop_id, ":enemy_party_leader", "p_encountered_party_backup", 0),
         (is_between, ":enemy_party_leader", kingdom_heroes_begin, kingdom_heroes_end),
         (call_script, "script_add_log_entry", logent_lord_helped_by_player, "trp_player",  -1, ":enemy_party_leader", -1),
       (try_end),
       ]],
]
