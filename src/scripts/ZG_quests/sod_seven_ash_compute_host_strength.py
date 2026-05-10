SCRIPTS = [
("sod_seven_ash_compute_host_strength",
    [
      (store_script_param, ":player_field_strength", 1),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_player_strength_siege, ":player_field_strength"),

      # Design formula: base 140 + twice the visible player field strength,
      # clamped to 180-420 so Wulfred feels adaptive without infinite scaling.
      (assign, ":host_strength", 140),
      (store_mul, ":scaled_player_strength", ":player_field_strength", 2),
      (val_add, ":host_strength", ":scaled_player_strength"),
      (val_max, ":host_strength", 180),
      (val_min, ":host_strength", 420),

      # Elite core scales more gently and stays readable for mission waves.
      (store_div, ":elite_core", ":player_field_strength", 3),
      (val_add, ":elite_core", 35),
      (val_max, ":elite_core", 45),
      (val_min, ":elite_core", 90),

      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_wulfred_host_strength, ":host_strength"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_wulfred_elite_core, ":elite_core"),
      (assign, reg0, ":host_strength"),
      (assign, reg1, ":elite_core"),
  ]),
]
