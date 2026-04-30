SCRIPTS = [
("update_titles",
    [
      (call_script, "script_generate_titles"),
      (try_for_range, ":troop", kingdom_heroes_begin, kingdom_heroes_end),
		(troop_get_slot, ":cur_party", ":troop", slot_troop_leaded_party),
		(gt, ":cur_party", 0),
        (call_script, "script_store_troop_name_fief", s5, ":troop"),
        (party_set_name, ":cur_party", s5),
      (try_end),
      (call_script, "script_update_merc_names"),
  ]),
]
