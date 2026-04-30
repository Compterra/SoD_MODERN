SCRIPTS = [
("center_get_food_store_limit",
    [
      (store_script_param_1, ":center_no"),
      (assign, ":food_store_limit", 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (assign, ":food_store_limit", town_food_limit),
      (else_try),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":food_store_limit", castle_food_limit),
      (try_end),
      (assign, reg0, ":food_store_limit"),
  ]),
]
