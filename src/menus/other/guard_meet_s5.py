MENUS = [
(
    "castle_meeting", mnf_enable_hot_keys,
    "With whom do you want to meet?",
    "none",
    [
      (assign, "$num_castle_meeting_troops", 0),
      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (call_script, "script_get_troop_attached_party", ":troop_no"),
        (eq, "$g_encountered_party", reg0),
        (troop_set_slot, "trp_temp_array_a", "$num_castle_meeting_troops", ":troop_no"),
        (val_add, "$num_castle_meeting_troops", 1),
      (try_end),
      (set_background_mesh, "$g_sod_town_background"),
    ],
    [
      ("guard_meet_s5", [(gt, "$num_castle_meeting_troops", 0), (troop_get_slot, ":troop_no", "trp_temp_array_a", 0), (call_script, "script_store_troop_name", s5, ":troop_no")],
       "{s5}.", [(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 0), (jump_to_menu, "mnu_castle_meeting_selected")]),
      ("guard_meet_s5_2", [(gt, "$num_castle_meeting_troops", 1), (troop_get_slot, ":troop_no", "trp_temp_array_a", 1), (call_script, "script_store_troop_name", s5, ":troop_no")],
       "{s5}.", [(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 1), (jump_to_menu, "mnu_castle_meeting_selected")]),
      ("guard_meet_s5_3", [(gt, "$num_castle_meeting_troops", 2), (troop_get_slot, ":troop_no", "trp_temp_array_a", 2), (call_script, "script_store_troop_name", s5, ":troop_no")],
       "{s5}.", [(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 2), (jump_to_menu, "mnu_castle_meeting_selected")]),
      ("guard_meet_s5_4", [(gt, "$num_castle_meeting_troops", 3), (troop_get_slot, ":troop_no", "trp_temp_array_a", 3), (call_script, "script_store_troop_name", s5, ":troop_no")],
       "{s5}.", [(troop_get_slot, "$castle_meeting_selected_troop", "trp_temp_array_a", 3), (jump_to_menu, "mnu_castle_meeting_selected")]),

      ("forget_it", [],
       "Forget it.",
       [(jump_to_menu, "mnu_castle_guard")]),
    ]
  ),
]
