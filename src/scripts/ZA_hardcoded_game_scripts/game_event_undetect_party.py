SCRIPTS = [
("game_event_undetect_party",
    [
      (store_script_param_1, ":party_id"),
      (try_begin),
        (party_slot_eq, ":party_id", slot_party_type, spt_kingdom_hero_party),
        (party_stack_get_troop_id, ":leader", ":party_id", 0),
        (is_between, ":leader", kingdom_heroes_begin, kingdom_heroes_end),
        (call_script, "script_update_troop_location_notes", ":leader", 0),
      (try_end),
  ]),
]
