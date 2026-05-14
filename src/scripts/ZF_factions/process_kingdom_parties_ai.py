SCRIPTS = [
("process_kingdom_parties_ai",
    [
      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (gt, ":party_no", 0),
        (party_is_active, ":party_no"),
		(party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party), #twan453 exclude mercs
        (call_script, "script_process_hero_ai", ":troop_no"),
      (try_end),
  ]),
]
