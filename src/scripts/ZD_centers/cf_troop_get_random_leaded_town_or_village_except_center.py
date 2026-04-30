SCRIPTS = [
("cf_troop_get_random_leaded_town_or_village_except_center",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":except_center_no"),

      (assign, ":num_centers", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (neq, ":center_no", ":except_center_no"),
        (val_add, ":num_centers", 1),
      (try_end),

      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
      (assign, ":end_cond", centers_end),
      (try_for_range, ":center_no", centers_begin, ":end_cond"),
        (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (neq, ":center_no", ":except_center_no"),
        (val_sub, ":random_center", 1),
        (lt, ":random_center", 0),
        (assign, ":target_center", ":center_no"),
        (assign, ":end_cond", 0),
      (try_end),
      (assign, reg0, ":target_center"),
  ]),
]
