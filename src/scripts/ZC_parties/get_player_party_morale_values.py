SCRIPTS = [
("get_player_party_morale_values",
    [
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (assign, ":num_men", 0),
      (try_for_range, ":i_stack", 1, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          #MORDACHAI - reduce the negative morale of a hero
          (val_add, ":num_men", 1),
        (else_try),
          (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
          (val_add, ":num_men", ":stack_size"),
        (try_end),
      (try_end),

      #MORDACHAI - reduce the effect of party size on morale to 2/3
      (val_mul, ":num_men", 2),
      (val_div, ":num_men", 3),

      (assign, "$g_player_party_morale_modifier_party_size", ":num_men"),

      (store_skill_level, ":player_leadership", "skl_leadership", "trp_player"),
      #MORDACHAI - increase morale boost to leadership x 10 (was x 7)
      (store_mul, "$g_player_party_morale_modifier_leadership", ":player_leadership", 10),
      (assign, ":new_morale", "$g_player_party_morale_modifier_leadership"),
      (val_sub, ":new_morale", "$g_player_party_morale_modifier_party_size"),
      (val_add, ":new_morale", 50),

      (assign, "$g_player_party_morale_modifier_food", 0),
      (try_for_range, ":cur_edible", food_begin, food_end),
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_edible", imod_rotten),
        (item_get_slot, ":food_bonus", ":cur_edible", slot_item_food_bonus),
        (val_add, "$g_player_party_morale_modifier_food", ":food_bonus"),
      (try_end),
      (val_add, ":new_morale", "$g_player_party_morale_modifier_food"),

      (try_begin),
        (eq, "$g_player_party_morale_modifier_food", 0),
        (assign, "$g_player_party_morale_modifier_no_food", 30),
        (val_sub, ":new_morale", "$g_player_party_morale_modifier_no_food"),
      (else_try),
        (assign, "$g_player_party_morale_modifier_no_food", 0),
      (try_end),

      (assign, "$g_player_party_morale_modifier_debt", 0),
      (try_begin),
        (val_max, "$g_player_debt_to_party_members", 0),
        (gt, "$g_player_debt_to_party_members", 0),
        (call_script, "script_calculate_player_faction_wage"),
        (assign, ":total_wages", reg0),
        (gt, ":total_wages", 0),
        (store_mul, "$g_player_party_morale_modifier_debt", "$g_player_debt_to_party_members", 10),
        (val_div, "$g_player_party_morale_modifier_debt", ":total_wages"),
        (val_clamp, "$g_player_party_morale_modifier_debt", 1, 31),
        (val_sub, ":new_morale", "$g_player_party_morale_modifier_debt"),
      (try_end),

      (val_clamp, ":new_morale", 0, 101),
      (assign, reg0, ":new_morale"),
  ]),
]
