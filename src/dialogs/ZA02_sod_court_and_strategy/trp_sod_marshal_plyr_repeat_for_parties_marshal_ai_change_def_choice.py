DIALOGS = [
[trp_sod_marshal|plyr|repeat_for_parties, "marshal_ai_change_def_choice",
   [
   (store_repeat_object, ":center_no"),
   (is_between, ":center_no", centers_begin, centers_end),
   (store_faction_of_party, ":center_fac", ":center_no"),
   (eq, ":center_fac", "fac_player_supporters_faction"),
   (str_store_party_name, s1, ":center_no")
     ],
   "{s1} region.", "marshal_ai",
   [(store_repeat_object, ":center_no"),
   (faction_set_slot, "fac_player_supporters_faction", slot_faction_defensive_objective, ":center_no"),
   ]
   ],
]
