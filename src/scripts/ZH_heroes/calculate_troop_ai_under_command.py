SCRIPTS = [
("calculate_troop_ai_under_command",
    [
      (store_script_param, ":troop_no", 1),
      (try_begin),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (gt, ":party_no", 0),
        (party_slot_ge, ":party_no", slot_party_commander_party, 0),
        (party_set_ai_initiative, ":party_no", 50),
        (call_script, "script_party_decide_next_ai_state_under_command", ":party_no"),
      (try_end),
  ]),
]
