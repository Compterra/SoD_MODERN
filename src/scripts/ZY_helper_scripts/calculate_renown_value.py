SCRIPTS = [
("calculate_renown_value",
    [
      (call_script, "script_party_calculate_strength", "p_main_party", 0),
      (assign, ":main_party_strength", reg0),
      (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
      (assign, ":enemy_strength", reg0),
      (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
      (assign, ":friends_strength", reg0),

      (val_add, ":friends_strength", 1),
      (store_mul, ":enemy_strength_ratio", ":enemy_strength", 100),
      (val_div, ":enemy_strength_ratio", ":friends_strength"),

      (assign, ":renown_val", ":enemy_strength"),
      (val_mul, ":renown_val", ":enemy_strength_ratio"),
      (val_div, ":renown_val", 100),

      (val_mul, ":renown_val", ":main_party_strength"),
      (val_div, ":renown_val", ":friends_strength"),

      (store_div, "$battle_renown_value", ":renown_val", 5),
      (val_min, "$battle_renown_value", 2500),
      (convert_to_fixed_point, "$battle_renown_value"),
      (store_sqrt, "$battle_renown_value", "$battle_renown_value"),
      (convert_from_fixed_point, "$battle_renown_value"),
      (assign, reg8, "$battle_renown_value"),
      (display_message, "@Renown value for this battle is {reg8}.", renown_color),
  ]),
]
