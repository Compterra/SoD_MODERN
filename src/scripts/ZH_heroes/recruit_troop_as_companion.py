SCRIPTS = [
("recruit_troop_as_companion",
    [
      (store_script_param_1, ":troop_no"),
      (troop_set_slot, ":troop_no", slot_troop_occupation, slto_player_companion),
      (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
      (troop_set_auto_equip, ":troop_no", 0),
      (party_force_add_members, "p_main_party", ":troop_no", 1),
      (store_character_level, ":current_level", ":troop_no"),
      (troop_set_slot, ":troop_no", slot_troop_level_up, ":current_level"),
      (call_script, "script_store_troop_name_link", s6, ":troop_no"),
      (display_message, "@{s6} has joined your party", bannana),
  ]),
]
