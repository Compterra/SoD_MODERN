DIALOGS = [
[anyone|plyr, "center_captured_lord_advice",
   [
     (call_script, "script_print_troop_owned_centers_in_numbers_to_s0", "trp_player"),
     (str_store_party_name, s1, "$g_center_taken_by_player_faction"),
    ],
   "Please {s65}, I want to have {s1} for myself. (fiefs: {s0})", "center_captured_lord_advice_2",
   [
     (assign, "$temp", "trp_player"),
     ]],
]
