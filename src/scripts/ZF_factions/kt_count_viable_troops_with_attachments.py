SCRIPTS = [
( "kt_count_viable_troops_with_attachments",
   [
      # remember our params and set some initial values
      (store_script_param_1, ":root_party"),
      (store_script_param_2, ":exclude_leader"),

      # call the counting script for the given party
      (assign, ":attached_count", 0),
      (call_script, "script_kt_count_viable_troops", ":root_party", ":exclude_leader"),
      (assign, ":count_so_far", reg0),

      # for every attached party, do the same      
      (try_begin),
         (gt, ":root_party", 0),
         (party_is_active, ":root_party"),
         (party_get_num_attached_parties, ":attached_count", ":root_party"),
         (try_for_range, ":rank", 0, ":attached_count"),
            (party_get_attached_party_with_rank, ":attached_party", ":root_party", ":rank"),
            (call_script, "script_kt_count_viable_troops", ":attached_party", 0),
            (val_add, ":count_so_far", reg0),
         (try_end),
      (try_end),

      # fill out our returns
      (assign, reg0, ":count_so_far"),
      (assign, reg1, ":attached_count"),
   ]),
]
