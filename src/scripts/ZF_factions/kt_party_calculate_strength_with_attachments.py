SCRIPTS = [
( "kt_party_calculate_strength_with_attachments",
   [
      # remember our params and set some initial values
      (store_script_param_1, ":root_party"),
      (store_script_param_2, ":exclude_leader"),
      (store_script_param, ":is_siege", 3),

      # call the counting script for the given party
      (call_script, "script_kt_party_calculate_strength", ":root_party", ":exclude_leader", ":is_siege"),
      (assign, ":strength_so_far", reg0),
      (assign, ":def_so_far", reg1),
      (assign, ":count_so_far", reg2),
      (val_mul, ":def_so_far", ":count_so_far"),

      # for every attached party, do the same      
      (party_get_num_attached_parties, ":attached_count", ":root_party"),
      (try_for_range, ":rank", 0, ":attached_count"),
         (party_get_attached_party_with_rank, ":attached_party", ":root_party", ":rank"),
         (call_script, "script_kt_party_calculate_strength", ":attached_party", 0, ":is_siege"),
         (val_add, ":strength_so_far", reg0),
         (store_mul, ":def_this_party", reg1, reg2),
         (val_add, ":def_so_far", ":def_this_party"),
         (val_add, ":count_so_far", reg2),
      (try_end),

      # fill out our returns
      (assign, reg0, ":strength_so_far"),
      (val_div, ":def_so_far", ":count_so_far"),
      (assign, reg1, ":def_so_far"),      
      (assign, reg2, ":count_so_far"),
   ]),
]
