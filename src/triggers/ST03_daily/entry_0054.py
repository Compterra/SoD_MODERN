SIMPLE_TRIGGERS = [
(24,
   [
    # only consume food if the player isn't a captive
    (eq, "$g_player_is_captive", 0),

    # determine the number of troops with the player
    (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
    (assign, ":num_men", 0),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
      (val_add, ":num_men", ":stack_size"),
    (try_end),

    #MORDACHAI - one unit of food per 5 troops (instead of per 3 troops)
    (store_div, ":consumption_amount", ":num_men", 5),
    (val_max, ":consumption_amount", 1),

    (assign, ":no_food_displayed", 0),
    (try_for_range, ":unused", 0, ":consumption_amount"),
      (assign, ":available_food", 0),
      (try_for_range, ":cur_food", food_begin, food_end),
        (item_set_slot, ":cur_food", slot_item_is_checked, 0),
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_food", imod_rotten),
        (val_add, ":available_food", 1),
      (try_end),
      (try_begin),
        (gt, ":available_food", 0),
        (store_random_in_range, ":selected_food", 0, ":available_food"),
        (call_script, "script_consume_food", ":selected_food"),
      (else_try),
        (eq, ":no_food_displayed", 0),
        (display_message, "@Your party has no food left!", red),
        (call_script, "script_change_player_party_morale", -3),
        (assign, ":no_food_displayed", 1),
        #NPC companion changes begin
        (try_begin),
            (call_script, "script_party_count_fit_regulars", "p_main_party"),
            (gt, reg0, 0),
            (call_script, "script_objectionable_action", tmt_egalitarian, "str_men_hungry"),
        (try_end),
        #NPC companion changes end
      (try_end),
    (try_end),

    # MORDACHAI: warn the player when they're down to less than three days of rations
    (try_begin),
      (eq, ":no_food_displayed", 0),
      (call_script, "script_count_edible_food"),
      (store_mul, reg1, ":consumption_amount", 3),
      (lt, reg0, reg1),
      (display_message, "@Your stores are running low.", warning_color),
    (try_end),

    # debug
    (try_begin),
      (eq, "$g_sod_debug", 1),
      (call_script, "script_count_edible_food"),
      (assign, reg1, ":consumption_amount"),
      (lt, reg0, reg1),
      (display_message, "@The party is consuming {reg1} provisions each day. {reg0} remain.", debug_color),
    (try_end),
  ]),
]
