DIALOGS = [
[anyone|plyr, "center_captured_lord_advice",
   [
     (call_script, "script_print_troop_owned_centers_in_numbers_to_s0", "$g_talk_troop"),
     (str_store_party_name, s1, "$g_center_taken_by_player_faction"),
     ],
   "{s66}, you should have {s1} for yourself. (fiefs: {s0})", "center_captured_lord_advice_2",
   [
     (assign, "$temp", "$g_talk_troop"),
     ]],
]
