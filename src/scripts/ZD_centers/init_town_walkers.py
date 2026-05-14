SCRIPTS = [
("init_town_walkers",
    [(try_begin),
        (eq, "$town_nighttime", 0),
        (try_for_range, ":walker_no", 0, num_town_walkers),
          (store_add, ":troop_slot", slot_center_walker_0_troop, ":walker_no"),
          (party_get_slot, ":walker_troop_id", "$current_town", ":troop_slot"),
          (gt, ":walker_troop_id", 0),
          (store_add, ":entry_no", town_walker_entries_start, ":walker_no"),
          (set_visitor, ":entry_no", ":walker_troop_id"),
        (try_end),
    ]),
]
