SCRIPTS = [
("get_faction_temptation_factor",
     [(store_script_param_1, ":kingdom_no"),
      (faction_get_slot, ":economic_strength", ":kingdom_no", slot_faction_economic_strength),
      (faction_get_slot, ":power", ":kingdom_no", slot_faction_current_power),
      (val_mul, ":economic_strength", 100),
      (val_div, ":economic_strength", ":power"),
      (assign, reg0, ":economic_strength"),
      ]),
]
