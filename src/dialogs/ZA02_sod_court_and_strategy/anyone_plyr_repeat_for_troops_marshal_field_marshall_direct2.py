DIALOGS = [
[anyone|plyr|repeat_for_troops, "marshal_field_marshall_direct2",
    [
      (store_repeat_object, ":troop_no"),
      (is_between, ":troop_no", heroes_begin, heroes_end),
      (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
      (store_troop_faction, ":faction_no", ":troop_no"),
      (eq, ":faction_no", "fac_player_supporters_faction"),
      (call_script, "script_store_troop_name", s31, ":troop_no")
    ],
    "{s31}", "marshal_field_marshall_direct3",
    [
      (store_repeat_object, ":new_marshall"),
	  (faction_set_slot, "fac_player_supporters_faction", slot_faction_marshall, ":new_marshall"),
      (call_script, "script_change_player_relation_with_troop", ":new_marshall", 5),
	  (call_script, "script_update_titles"),
    ]
  ],
]
