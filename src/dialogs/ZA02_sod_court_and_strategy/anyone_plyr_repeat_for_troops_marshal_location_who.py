DIALOGS = [
[anyone|plyr|repeat_for_troops, "marshal_location_who",
    [
      (store_repeat_object, ":troop_no"),
      (is_between, ":troop_no", heroes_begin, heroes_end),
      (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
      (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
      (store_troop_faction, ":faction_no", ":troop_no"),
      (eq, ":faction_no", "fac_player_supporters_faction"),
      (call_script, "script_store_troop_name", s1, ":troop_no")
    ],
    "{s1}", "marshal_location_show",
    [
      (store_repeat_object, "$hero_requested_to_learn_location"),
    ]
  ],
]
