DIALOGS = [
[anyone , "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
                     (neq, "$g_talk_troop_met", 0),
                     (gt, "$g_time_since_last_talk", 24),
                     (gt, "$g_talk_troop_relation", -10),
                     (store_random_in_range, ":random_num", 0, 100),
                     (lt, ":random_num", 30),
                     (eq, "$talk_context", tc_town_talk),
                     (call_script, "script_cf_troop_get_random_enemy_troop_with_occupation", "$g_talk_troop", slto_kingdom_hero),
                     (assign, ":other_lord", reg0),
                     (troop_get_slot, ":other_lord_relation", ":other_lord", slot_troop_player_relation),
                     (ge, ":other_lord_relation", 20),
                     (call_script, "script_store_troop_name", s6, ":other_lord"),
                     (assign, "$temp", ":other_lord"),
                     ],
   "I heard that you have befriended that {s43} called {s6}.\
 Believe me, you can't trust that man.\
 You should end your dealings with him.", "lord_event_choose_friend", [
    (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_insult_default"),

     ]],
]
