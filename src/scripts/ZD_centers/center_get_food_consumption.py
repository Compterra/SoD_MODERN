SCRIPTS = [
("center_get_food_consumption",
    [
      (store_script_param_1, ":center_no"),

      # get the number of combatants and prisoners garrisoned here
      (party_get_num_companions, ":military", ":center_no"),
      (party_get_num_prisoners, ":prisoners", ":center_no"),

      # and all other garrisoned parties
      (party_get_num_attached_parties, ":num_parties",  ":center_no"),
      (try_for_range, ":index", 0, ":num_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":center_no", ":index"),
        (party_get_num_companions, reg0, ":attached_party"),
        (val_add, ":military", reg0),
        (party_get_num_prisoners, reg0, ":attached_party"),
        (val_add, ":prisoners", reg0),
      (try_end),

      # add civilian population (SOD only)
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (party_get_slot, ":civilians", ":center_no", slot_center_sod_local_population),
      (else_try),
        # consider castles to have a skeleton number of non-combatants around
        (assign, ":civilians", 10),
      (try_end),

      # military troops are on 3/4 rations
      (store_mul, ":mil_rate", ":military", 3),
      (val_div, ":mil_rate", 4),

      # civilians are on 1/2 rations
      (store_div, ":civ_rate", ":civilians", 2),

      # prisoners are on 1/4 rations
      (store_div, ":prs_rate", ":prisoners", 4),

      # and voila: the consumption rate (return it via reg0)
      (store_add, reg0, ":mil_rate", ":civ_rate"),
      (val_add, reg0, ":prs_rate"),

      #DEBUG
      (try_begin),
        (eq, "$g_sod_debug", 1),
        (assign, reg1, ":military"),
        (assign, reg2, ":mil_rate"),
        (assign, reg3, ":civilians"),
        (assign, reg4, ":civ_rate"),
        (assign, reg5, ":prisoners"),
        (assign, reg6, ":prs_rate"),
        (str_store_party_name_link, s1, ":center_no"),
        (display_message, "@Food Consumption {s1}: ({reg1}x.75 = {reg2}) + ({reg3}x.5 = {reg4}) + ({reg5}x.25 = {reg6}) = {reg0}", debug_color),
      (try_end),
  ]),
]
