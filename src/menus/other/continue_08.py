MENUS = [
(
    "join_order_attack", mnf_disable_all_keys,
    "{s4}^^Your casualties: {s8}^^Allies' casualties: {s9}^^Enemy casualties: {s10}",
    "none",
    [
      (set_background_mesh, "mesh_pic_involve"),

      (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
      (assign, ":player_party_strength", reg0),
      (val_div, ":player_party_strength", 5),
      (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
      (assign, ":friend_party_strength", reg0),
      (val_div, ":friend_party_strength", 5),
      (val_max, ":friend_party_strength", 1),

      (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
      (assign, ":enemy_party_strength", reg0),
      (val_div, ":enemy_party_strength", 5),

      (assign, ":enemy_party_strength_for_p", ":enemy_party_strength"),
      (val_mul, ":enemy_party_strength_for_p", ":player_party_strength"),
      (val_div, ":enemy_party_strength_for_p", ":friend_party_strength"),

      (val_sub, ":enemy_party_strength", ":enemy_party_strength_for_p"),
      (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength_for_p", "p_temp_casualties"),
      (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
      (str_store_string_reg, s8, s0),

      (try_begin),
        (gt, "$g_enemy_party", 0),
        (party_is_active, "$g_enemy_party"),
        (inflict_casualties_to_party_group, "$g_enemy_party", ":friend_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s10, s0),
        (party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),
      (else_try),
        (str_store_string, s10, "@None"),
      (try_end),

      (call_script, "script_collect_friendly_parties"),
#      (party_collect_attachments_to_party, "$g_ally_party", "p_collective_ally"),

      (try_begin),
        (gt, "$g_ally_party", 0),
        (party_is_active, "$g_ally_party"),
        (inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s9, s0),
      (else_try),
        (str_store_string, s9, "@None"),
      (try_end),

#      (assign, "$cant_leave_encounter", 0),
      (assign, "$no_soldiers_left", 0),
      (try_begin),
        (call_script, "script_party_count_members_with_full_health", "p_main_party"),
        (le, reg(0), 0),
        (assign, "$no_soldiers_left", 1),
        (str_store_string, s4, "str_join_order_attack_failure"),
      (else_try),
        (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
        (le, reg(0), 0),
        (assign, "$g_battle_result", 1),
        (assign, "$no_soldiers_left", 1),
        (str_store_string, s4, "str_join_order_attack_success"),
      (else_try),
        (str_store_string, s4, "str_join_order_attack_continue"),
      (try_end),
    ],
    [
      ("continue", [], "Continue...", [(jump_to_menu, "mnu_join_battle"),]),
    ]
  ),
]
