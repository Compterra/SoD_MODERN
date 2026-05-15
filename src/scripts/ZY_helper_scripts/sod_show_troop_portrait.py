# COST: trivial
SCRIPTS = [
("sod_show_troop_portrait",
  [
    (store_script_param, ":troop_no", 1),

    (try_begin),
      (is_between, ":troop_no", 0, "trp_last_troop"),
      (set_fixed_point_multiplier, 100),
      (init_position, pos0),
      (position_set_x, pos0, 70),
      (position_set_y, pos0, 5),
      (position_set_z, pos0, 75),
      (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":troop_no", pos0),
    (try_end),
  ]),

("sod_show_party_leader_portrait",
  [
    (store_script_param, ":party_no", 1),

    (try_begin),
      (gt, ":party_no", 0),
      (party_is_active, ":party_no"),
      (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
      (gt, ":num_stacks", 0),
      (party_stack_get_troop_id, ":leader_troop", ":party_no", 0),
      (call_script, "script_sod_show_troop_portrait", ":leader_troop"),
    (try_end),
  ]),
]
