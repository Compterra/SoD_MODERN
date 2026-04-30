SCRIPTS = [
("update_merc_names",
    [
      (try_for_parties, ":cur_party"),
        (party_slot_eq, ":cur_party", slot_party_type, spt_ai_mercenaries),
        (party_get_slot, ":troop", ":cur_party", slot_party_boss),
		(is_between, ":troop", kingdom_heroes_begin, kingdom_heroes_end),
        (call_script, "script_store_troop_name", s5, ":troop"),
        (party_set_name, ":cur_party", "str_s5_mercs"),
      (try_end),
  ]),
]
