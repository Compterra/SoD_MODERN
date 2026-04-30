MENUS = [
(
    "encounter_retreat", mnf_enable_hot_keys,
    "You tell {reg4} of your troops to hold the enemy while you retreat with the rest of your party.",
    "none",
    [
      (set_background_mesh, "mesh_pic_retreat"),
    ],
    [
      ("continue", [], "Continue...", [
###Troop commentary changes begin
        (call_script, "script_objectionable_action", tmt_aristocratic, "str_flee_battle"),
        (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
        (try_for_range, ":stack_no", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", "p_encountered_party_backup", ":stack_no"),
            (is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end),
            (store_troop_faction, ":victorious_faction", ":stack_troop"),
            (call_script, "script_add_log_entry", logent_player_retreated_from_lord_cowardly, "trp_player", -1, ":stack_troop", ":victorious_faction"),
        (try_end),
###Troop commentary changes end

        (leave_encounter), (change_screen_return)]),
     ]
  ),
]
