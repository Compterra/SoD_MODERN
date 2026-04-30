MENUS = [
(
   "castle_attack_walls_simulate",
   mnf_scale_picture | mnf_disable_all_keys,
   "{s4}^^Your casualties:{s8}^^Enemy casualties were: {s9}^^Remaining allies: {reg10}^Remaining enemies: {reg11}",
   "none",
   [
      (troop_get_type, ":is_female", "trp_player"),
      (try_begin),
      (eq, ":is_female", 1),
      (set_background_mesh, "mesh_pic_siege_sighted_fem"),
      (else_try),
      (set_background_mesh, "mesh_pic_siege_sighted"),
      (try_end),

      (try_begin),
      (eq, "$g_sod_autoresolve", 1),

      # grab party strengths and weight for attackers and defenders
      (call_script, "script_kt_party_calculate_strength_with_attachments", "p_main_party", 1, 1), # skip player and is_siege
      (assign, ":p_str", reg0),
      (assign, ":p_def", reg1),
      (val_mul, ":p_str", 3),
      (val_div, ":p_str", 4), # attacker strength penalty
            
      (call_script, "script_kt_party_calculate_strength_with_attachments", "$g_encountered_party", 0, 1),
      (assign, ":e_str", reg0),
      (assign, ":e_def", reg1),
      (val_mul, ":e_str", 3),
      (val_div, ":e_str", 2),

      # adjust for defense values
      (val_mul, ":e_str", ":p_def"),
      (val_mul, ":p_str", ":e_def"),
      (val_div, ":e_str", 100),
      (val_div, ":p_str", 100),
      
      # slow the battle down so the player can make choices
      # attacking a castle goes faster than overland battles.
      (val_div, ":e_str", 10),
      (val_div, ":p_str", 10),
      
      # debughax
      (assign, reg0, ":e_str"),
      (assign, reg1, ":p_str"),
      (display_message, "@going to solver:  e_str:  {reg0}, p_str:  {reg1}", 0xFFFFFF00),
      
      # hurt both sides
      (inflict_casualties_to_party_group, "p_main_party", ":e_str", "p_temp_casualties"),
      (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
      (str_store_string_reg, s8, s0),

      (inflict_casualties_to_party_group, "$g_encountered_party", ":p_str", "p_temp_casualties"),
      (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
      (str_store_string_reg, s9, s0),  #KTO AUTORESOLVE END     

      (else_try), #native/improved native (same here)

      (call_script, "script_party_calculate_siege_or_not_strength", "p_main_party", 1), 
        (assign, ":player_party_strength", reg0),
        (val_div, ":player_party_strength", 10),

        (call_script, "script_party_calculate_siege_or_not_strength", "$g_encountered_party", 1),
        (assign, ":enemy_party_strength", reg0),
        (val_div, ":enemy_party_strength", 4),

        (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s8, s0),

        (inflict_casualties_to_party_group, "$g_encountered_party", ":player_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s9, s0),
      (try_end), # end resolve
       

      # fill out remaining troops
      (call_script, "script_kt_count_viable_troops_with_attachments", "p_main_party", 1), # don't count the player
      (assign, ":allies_left", reg0),
      (assign, reg10, reg0),
      (call_script, "script_kt_count_viable_troops_with_attachments", "$g_encountered_party", 0),      
      (assign, ":enemies_left", reg0),
      (assign, reg11, reg0),

      # determine if we're still fighting or what for the next menu      
      (assign, "$no_soldiers_left", 0),
      (try_begin),
         (le, ":allies_left", 0),
         (assign, "$no_soldiers_left", 1),
         (str_store_string, s4, "str_attack_walls_failure"),
      (else_try),
         (le, ":enemies_left", 0),
         (assign, "$no_soldiers_left", 1),
         (assign, "$g_battle_result", 1),
         (str_store_string, s4, "str_attack_walls_success"),
      (else_try),
         (str_store_string, s4, "str_attack_walls_continue"),
      (try_end),
   ],
   [
   ("continue",[],"Continue...",[(jump_to_menu,"mnu_castle_besiege")]),
   ]),
]
