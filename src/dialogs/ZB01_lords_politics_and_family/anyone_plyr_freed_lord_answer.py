DIALOGS = [
[anyone|plyr, "freed_lord_answer", [(lt, "$g_talk_troop_faction_relation", 0)],
   "You're not going anywhere, 'friend'. You're my prisoner now.", "freed_lord_answer_1",
   [(troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, "p_main_party"),
    (party_force_add_prisoners, "p_main_party", "$g_talk_troop", 1),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -30),
    (call_script, "script_change_player_relation_with_faction_ex", "$g_talk_troop_faction", -2),
    (call_script, "script_event_hero_taken_prisoner_by_player", "$g_talk_troop"),
    ]],
]
