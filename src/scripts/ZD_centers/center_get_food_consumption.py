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
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (call_script, "script_sod_get_center_population_capacity_profile", ":center_no"),
        (assign, ":civilians", reg9),
      (else_try),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (call_script, "script_sod_get_center_population_capacity_profile", ":center_no"),
        (assign, ":civilians", reg9),
      (else_try),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (call_script, "script_sod_get_center_population_capacity_profile", ":center_no"),
        (assign, ":civilians", reg9),
        (val_div, ":civilians", 20),
        (val_max, ":civilians", 10),
      (else_try),
        # consider castles to have a skeleton number of non-combatants around
        (assign, ":civilians", 10),
      (try_end),

      # military troops are on 3/4 rations
      (store_mul, ":mil_rate", ":military", 3),
      (val_div, ":mil_rate", 4),

      # civilians are on 1/2 rations
      (store_div, ":civ_rate", ":civilians", 2),
      (try_begin),
        # Towns are market engines: craftsmen, visitors, workshops, and dense
        # households consume more than rural civilian headcount alone suggests.
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (val_mul, ":civ_rate", 6),
        (val_div, ":civ_rate", 5),
        (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
        (val_max, ":prosperity", 0),
        (store_div, ":service_consumption", ":prosperity", 10),
        (val_add, ":civ_rate", ":service_consumption"),
      (try_end),

      # prisoners are on 1/4 rations
      (store_div, ":prs_rate", ":prisoners", 4),

      # and voila: the consumption rate (return it via reg0)
      (store_add, ":food_consumption", ":mil_rate", ":civ_rate"),
      (val_add, ":food_consumption", ":prs_rate"),
      (call_script, "script_sod_get_center_modifier", ":center_no", sod_center_modifier_food_consumption_pct),
      (val_mul, ":food_consumption", reg0),
      (val_div, ":food_consumption", 100),
      (val_max, ":food_consumption", 0),
      (assign, reg0, ":food_consumption"),

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
