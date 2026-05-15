MENUS = [
(
      "order_attack_2",mnf_disable_all_keys,
      "{s4}^^Your casualties: {s8}^^Enemy casualties: {s9}^^Allied line: {s10}^Enemy line: {s11}",
      "none",
      [
         (assign, ":encountered_party_valid", 0),
         (try_begin),
            (gt, "$g_encountered_party", 0),
            (party_is_active, "$g_encountered_party"),
            (assign, ":encountered_party_valid", 1),
         (else_try),
            (party_clear, "p_collective_enemy"),
         (try_end),

         (try_begin),
         (eq, "$g_sod_autoresolve", 1),
         # kt0:  heavily modified to use the new strength calculation stuff.
         # Antigravity: Fixed massive auto-resolve exploit! Automatically detect if the player is assaulting a Town/Castle.
         # The KT0 engine needs the correct '2' and '1' params to grant the AI defenders their huge wall multiplier.
         (assign, ":is_siege_atk", 0),
         (assign, ":is_siege_def", 0),
         (try_begin),
            (eq, ":encountered_party_valid", 1),
            (this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
            (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
            (assign, ":is_siege_atk", 2),
            (assign, ":is_siege_def", 1),
         (try_end),

         (call_script, "script_kt_party_calculate_strength", "p_main_party", 1, ":is_siege_atk"), # passing dynamic siege context
         (assign, ":player_party_strength", reg0),
         (assign, ":player_party_defense", reg1),
         
         (call_script, "script_kt_party_calculate_strength", "p_collective_enemy", 0, ":is_siege_def"), # passing dynamic siege context
         (assign, ":enemy_party_strength", reg0),
         (assign, ":enemy_party_defense", reg1),
         
         # normalize strengths for defense
         (val_mul, ":player_party_strength", ":enemy_party_defense"),
         (val_mul, ":enemy_party_strength", ":player_party_defense"),
         (val_div, ":player_party_strength", 100),
         (val_div, ":enemy_party_strength", 100),
         
         # slow down the fight so the player can make choices between each 
         # round.  note that player fights go faster than fights between AI
         # parties.  this is intentional:  it gives the player time to 
         # become involved.
         (val_div, ":player_party_strength", 25),
         (val_div, ":enemy_party_strength", 25),

         (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength", "p_temp_casualties"),
         (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
         (str_store_string_reg, s8, s0),

         (try_begin),
            (eq, ":encountered_party_valid", 1),
            (inflict_casualties_to_party_group, "$g_encountered_party", ":player_party_strength", "p_temp_casualties"),
            (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
            (str_store_string_reg, s9, s0),
            (party_collect_attachments_to_party, "$g_encountered_party", "p_collective_enemy"),  # KT0 IMPROVED AUTORESOLVE ENDS
         (else_try),
            (str_store_string, s9, "@None"),
         (try_end),

           
         (else_try),   # native/native improved autoresolve are the same here

         (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
         (assign, ":player_party_strength", reg0),
         (val_div, ":player_party_strength", 5),
         (call_script, "script_party_calculate_siege_or_not_strength", "p_collective_enemy", 0), # make sure outdoor strength is used
         (assign, ":enemy_party_strength", reg0),
         (val_div, ":enemy_party_strength", 5),
                                    
#                                    (call_script,"script_inflict_casualties_to_party", "p_main_party", ":enemy_party_strength"),
        (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s8, s0),
                                    
####                                    (call_script,"script_inflict_casualties_to_party", "$g_encountered_party", ":player_party_strength"),
        (try_begin),
          (eq, ":encountered_party_valid", 1),
          (inflict_casualties_to_party_group, "$g_encountered_party", ":player_party_strength", "p_temp_casualties"),
          (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
          (str_store_string_reg, s9, s0),
          (party_collect_attachments_to_party, "$g_encountered_party", "p_collective_enemy"),
        (else_try),
          (str_store_string, s9, "@None"),
        (try_end),

         (try_end),   # autoresolves end

        # calculate aftermath so we can display stuff
         (call_script, "script_party_count_members_with_full_health","p_main_party"),
         (assign, reg10, reg0),
         (call_script, "script_party_count_members_with_full_health","p_collective_enemy"),
         (assign, reg11, reg0),
         (try_begin),
            (le, reg10, 0),
            (str_store_string, s10, "@broken"),
         (else_try),
            (lt, reg10, 10),
            (str_store_string, s10, "@barely holding"),
         (else_try),
            (lt, reg10, 30),
            (str_store_string, s10, "@thinned but standing"),
         (else_try),
            (str_store_string, s10, "@still in force"),
         (try_end),
         (try_begin),
            (le, reg11, 0),
            (str_store_string, s11, "@broken"),
         (else_try),
            (lt, reg11, 10),
            (str_store_string, s11, "@wavering"),
         (else_try),
            (lt, reg11, 30),
            (str_store_string, s11, "@reduced but dangerous"),
         (else_try),
            (str_store_string, s11, "@still in force"),
         (try_end),

         (assign, "$no_soldiers_left", 0),
         (try_begin),
            (le, reg10, 0),
            (assign, "$no_soldiers_left", 1),
            (str_store_string, s4, "str_order_attack_failure"),
         (else_try),
            (le, reg11, 0),
            (assign, ":continue", 0),
            (party_get_num_companion_stacks, ":party_num_stacks", "p_collective_enemy"),
            (try_begin),
               (eq, ":party_num_stacks", 0),
               (assign, ":continue", 1),
            (else_try),
               (party_stack_get_troop_id, ":party_leader", "p_collective_enemy", 0),
               (try_begin),
                  (neg|troop_is_hero, ":party_leader"),
                  (assign, ":continue", 1),
               (else_try),
                  (troop_is_wounded, ":party_leader"),
                  (assign, ":continue", 1),
               (try_end),
            (try_end),
            (eq, ":continue", 1),
            (assign, "$g_battle_result", 1),
            (assign, "$no_soldiers_left", 1),
            (str_store_string, s4, "str_order_attack_success"),
         (else_try),
            (str_store_string, s4, "str_order_attack_continue"),                           # TWAN CHANGES END
         (try_end),
      ],
    [
      ("order_attack_continue",[(eq, "$no_soldiers_left", 0)],"Order your soldiers to continue the attack.",[
          (jump_to_menu,"mnu_order_attack_2"),
          ]),
      ("order_retreat",[(eq, "$no_soldiers_left", 0)],"Call your soldiers back.",[
          (jump_to_menu,"mnu_simple_encounter"),
          ]),
      ("continue",[(eq, "$no_soldiers_left", 1)],"Continue...",[
          (jump_to_menu,"mnu_simple_encounter"),
          ]),
    ]
  ),
]
