SCRIPTS = [
("store_average_center_value_per_faction",
        [
          (store_sub, ":num_towns", towns_end, towns_begin),
          (store_sub, ":num_castles", castles_end, castles_begin),
          (assign, ":num_factions", 0),
          (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
            (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
            (val_add, ":num_factions", 1),
          (try_end),
          (val_max, ":num_factions", 1),
          (store_mul, "$g_average_center_value_per_faction", ":num_towns", 2),
          (val_add, "$g_average_center_value_per_faction", ":num_castles"),
          (val_mul, "$g_average_center_value_per_faction", 10),
          (val_div, "$g_average_center_value_per_faction", ":num_factions"),
      ]),
]
