SCRIPTS = [
( "kt_party_calculate_strength",
   [
      # remember our params
      (store_script_param_1, ":party"),   # party id
      (store_script_param_2, ":exclude_leader"), # also a party id apparently
      (store_script_param, ":is_siege", 3), # 0 = open field, 1 = siege defender, 2 = siege attacker

      # clear out our returns and temps
      (assign, reg0, 0),
      (assign, reg1, 0),
      (assign, reg2, 0),

      # figure out which stack to start with and how many we have
      (party_get_num_companion_stacks, ":num_stacks", ":party"),
      (assign, ":first_stack", 0),
      (try_begin),
         (neq, ":exclude_leader", 0),
         (assign, ":first_stack", 1),
      (try_end),

      # for each stack that we care about, grab the offense, defense and count
      # and stuff the values into our return registers.
      (try_for_range, ":i_stack", ":first_stack", ":num_stacks"),
         (party_stack_get_troop_id, ":stack_troop", ":party", ":i_stack"),
         (party_stack_get_size, ":stack_size", ":party", ":i_stack"),
         (party_stack_get_num_wounded, ":num_wounded", ":party", ":i_stack"),
         (val_sub, ":stack_size", ":num_wounded"),
         (gt, ":stack_size", 0),

         (assign, ":o_val", 0),
         (assign, ":d_val", 0),
         (assign, ":h_val", 0),
         (assign, ":tr_type", kt_troop_type_footsoldier),

         (try_begin),
            # if this is not a hero, just read slots
            (neg|troop_is_hero, ":stack_troop"),
            (troop_get_slot, ":o_val", ":stack_troop", kt_slot_troop_o_val),
            (troop_get_slot, ":d_val", ":stack_troop", kt_slot_troop_d_val),
            (troop_get_slot, ":h_val", ":stack_troop", kt_slot_troop_h_val),
            (troop_get_slot, ":tr_type", ":stack_troop", kt_slot_troop_type),

            # mounted archers are support units; they don't get charge momentum.
            (try_begin),
               (eq, ":tr_type", kt_troop_type_mtdarcher),
               (assign, ":h_val", 0),
            (try_end),
         (else_try),
            # heroes get a level-based fallback and are treated by mount status.
            (store_character_level, ":level", ":stack_troop"),
            (store_mul, ":o_val", ":level", 3),
            (val_add, ":o_val", 50),
            (store_mul, ":d_val", ":level", 2),
            (val_add, ":d_val", 20),

            (troop_get_inventory_slot, ":horse_item", ":stack_troop", ek_horse),
            (try_begin),
               (ge, ":horse_item", 0),
               (assign, ":tr_type", kt_troop_type_cavalry),
               (assign, ":h_val", 50),
            (else_try),
               (assign, ":tr_type", kt_troop_type_footsoldier),
            (try_end),
         (try_end),

         # context-specific modifiers:
         #   0 = open field
         #   1 = defending a siege
         #   2 = attacking a siege
         (try_begin),
            (eq, ":is_siege", 1),
            (try_begin),
               (eq, ":tr_type", kt_troop_type_cavalry),
               (val_mul, ":o_val", 3),
               (val_div, ":o_val", 5),
               (val_mul, ":d_val", 3),
               (val_div, ":d_val", 5),
            (else_try),
               (eq, ":tr_type", kt_troop_type_archer),
               (val_mul, ":o_val", 4),
               (val_div, ":o_val", 3),
               (val_mul, ":d_val", 4),
               (val_div, ":d_val", 3),
            (else_try),
               (eq, ":tr_type", kt_troop_type_mtdarcher),
               (val_mul, ":o_val", 6),
               (val_div, ":o_val", 5),
               (val_mul, ":d_val", 6),
               (val_div, ":d_val", 5),
            (else_try),
               (eq, ":tr_type", kt_troop_type_footsoldier),
               (val_mul, ":o_val", 6),
               (val_div, ":o_val", 5),
               (val_mul, ":d_val", 6),
               (val_div, ":d_val", 5),
            (try_end),
         (else_try),
            (eq, ":is_siege", 2),
            (try_begin),
               (eq, ":tr_type", kt_troop_type_cavalry),
               (val_mul, ":o_val", 4),
               (val_div, ":o_val", 5),
               (val_mul, ":d_val", 4),
               (val_div, ":d_val", 5),
            (else_try),
               (eq, ":tr_type", kt_troop_type_archer),
               (val_mul, ":o_val", 6),
               (val_div, ":o_val", 5),
               (val_mul, ":d_val", 11),
               (val_div, ":d_val", 10),
            (else_try),
               (eq, ":tr_type", kt_troop_type_mtdarcher),
               (val_mul, ":o_val", 5),
               (val_div, ":o_val", 4),
               (val_mul, ":d_val", 11),
               (val_div, ":d_val", 10),
            (else_try),
               (eq, ":tr_type", kt_troop_type_footsoldier),
               (val_mul, ":o_val", 11),
               (val_div, ":o_val", 10),
               (val_mul, ":d_val", 11),
               (val_div, ":d_val", 10),
            (try_end),
         (else_try),
            (try_begin),
               (eq, ":tr_type", kt_troop_type_cavalry),
               (val_mul, ":o_val", 3),
               (val_div, ":o_val", 2),
               (val_mul, ":d_val", 3),
               (val_div, ":d_val", 2),
            (else_try),
               (eq, ":tr_type", kt_troop_type_archer),
               (val_mul, ":o_val", 6),
               (val_div, ":o_val", 5),
               (val_mul, ":d_val", 11),
               (val_div, ":d_val", 10),
            (else_try),
               (eq, ":tr_type", kt_troop_type_mtdarcher),
               (val_mul, ":d_val", 4),
               (val_div, ":d_val", 3),
            (else_try),
               (eq, ":tr_type", kt_troop_type_footsoldier),
               (val_mul, ":o_val", 11),
               (val_div, ":o_val", 10),
               (val_mul, ":d_val", 11),
               (val_div, ":d_val", 10),
            (try_end),
         (try_end),

         # charge momentum only matters in open-field fights.
         (try_begin),
            (eq, ":is_siege", 0),
            (val_add, ":o_val", ":h_val"),
         (try_end),

         # scale by surviving troop count and accumulate.
         (val_mul, ":o_val", ":stack_size"),
         (val_mul, ":d_val", ":stack_size"),
         (val_add, reg0, ":o_val"),
         (val_add, reg1, ":d_val"),
         (val_add, reg2, ":stack_size"),
      (try_end),

      # calculate damage redux from defense
      (try_begin),
         (gt, reg2, 0),
         (val_div, reg1, reg2), # avg defense
      (try_end),
      (val_clamp, reg1, 0, 90), # values outside this range don't work well
      (store_sub, reg1, 100, reg1), # opponent offense should be multiplied by this %
  ]),
]
