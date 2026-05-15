SCRIPTS = [
("update_companion_candidates_in_taverns",
      [
        (try_for_range, ":troop_no", companions_begin, companions_end),
          (troop_slot_eq, ":troop_no", slot_troop_occupation, 0),
          (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
          (assign, ":found_town", 0),

          (try_for_range, ":unused", 0, 12),
            (eq, ":found_town", 0),
            (store_random_in_range, ":town_no", towns_begin, towns_end),
            (neg|troop_slot_eq, ":troop_no", slot_troop_home, ":town_no"),
            (neg|troop_slot_eq, ":troop_no", slot_troop_first_encountered, ":town_no"),
            (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"),
            (assign, ":found_town", 1),
          (try_end),

          (try_begin),
            (eq, ":found_town", 0),
            (store_random_in_range, ":town_no", towns_begin, towns_end),
            (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"),
            (assign, ":found_town", 1),
          (try_end),

        (try_end),
    ]),
]
