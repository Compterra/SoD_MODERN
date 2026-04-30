SCRIPTS = [
("update_mercenary_units_of_towns",
      [(try_for_range, ":town_no", towns_begin, towns_end),
          (store_random_in_range, ":troop_no", mercenary_troops_begin, mercenary_troops_end),
          (party_set_slot, ":town_no", slot_center_mercenary_troop_type, ":troop_no"),
          (store_random_in_range, ":amount", 3, 8),
          (party_get_slot, ":pop", ":town_no", slot_center_sod_local_population),
          (val_sub, ":pop", town_pop_min),
          (val_max, ":pop", 0),
          (val_min, ":amount", ":pop"),
          (party_set_slot, ":town_no", slot_center_mercenary_troop_amount, ":amount"),
        (try_end),
    ]),
]
