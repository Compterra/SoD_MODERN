DIALOGS = [
[trp_sod_marshal|plyr|repeat_for_parties, "marshal_ai_change_off_choice",
   [
   (store_repeat_object, ":center_no"),
   (is_between, ":center_no", walled_centers_begin, walled_centers_end),
   (store_faction_of_party, ":center_fac", ":center_no"),
   (neq, ":center_fac", "fac_player_supporters_faction"),
   (store_relation, ":rln", ":center_fac", "fac_player_supporters_faction"),
   (lt, ":rln", 0),
   (str_store_party_name, s1, ":center_no")
     ],
   "{s1} region.", "marshal_ai",
   [(store_repeat_object, ":center_no"),
   (faction_set_slot, "fac_player_supporters_faction", slot_faction_offensive_objective, ":center_no"),
   ]
   ],
]
