DIALOGS = [
[anyone|plyr, "freed_lord_answer", [],
   "You are free to go wherever you want, sir.", "freed_lord_answer_2",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 7),
    (call_script, "script_change_player_honor", 2),
    (call_script, "script_change_player_relation_with_faction_ex", "$g_talk_troop_faction", 2)]],
]
