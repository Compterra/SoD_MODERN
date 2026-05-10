DIALOGS = [
[anyone|plyr, "defeat_lord_answer", [
  (neg|is_between, "$g_talk_troop", "trp_knight_6_01", "trp_black_army_leader_1"),
  (neq, "$g_talk_troop", "trp_kingdom_6_lord"),
  ],
   "You have fought well. You are free to go.", "defeat_lord_answer_2",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 5),
    (call_script, "script_sod_nemesis_note_lord_resolution", "$g_talk_troop", sod_nemesis_lord_resolution_mercy),
    (call_script, "script_change_player_honor", 3),
    (call_script, "script_sod_diplomacy_record_event", "$g_talk_troop_faction", sod_diplomacy_memory_released_lord, 1),
    (call_script, "script_add_log_entry", logent_lord_defeated_but_let_go_by_player, "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction")]],
]
