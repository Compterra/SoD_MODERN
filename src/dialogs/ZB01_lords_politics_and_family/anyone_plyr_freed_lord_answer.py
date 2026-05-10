DIALOGS = [
[anyone|plyr, "freed_lord_answer", [(lt, "$g_talk_troop_faction_relation", 0)],
   "You're not going anywhere, 'friend'. You're my prisoner now.", "freed_lord_answer_1",
   [(call_script, "script_sod_player_capture_hero_to_reg", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -30),
    (call_script, "script_change_player_relation_with_faction_ex", "$g_talk_troop_faction", -2),
    ]],
]
