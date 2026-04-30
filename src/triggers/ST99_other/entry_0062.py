SIMPLE_TRIGGERS = [
(72,
   [(call_script, "script_update_mercenary_units_of_towns"),
    #NPC changes begin
    # removes   (call_script, "script_update_companion_candidates_in_taverns"),
    #NPC changes end
    (call_script, "script_update_ransom_brokers"),
    (call_script, "script_update_tavern_travelers"),
    (call_script, "script_update_tavern_minstels"),
    (call_script, "script_update_booksellers"),
    (call_script, "script_update_villages_infested_by_bandits"),
    (try_for_range, ":village_no", villages_begin, villages_end),
      (call_script, "script_update_volunteer_troops_in_village", ":village_no"),
      (call_script, "script_update_npc_volunteer_troops_in_village", ":village_no"),
    (try_end),
    ]),
]
