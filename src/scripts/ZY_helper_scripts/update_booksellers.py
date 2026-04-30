SCRIPTS = [
("update_booksellers",
      [(try_for_range, ":town_no", towns_begin, towns_end),
          (party_set_slot, ":town_no", slot_center_tavern_bookseller, 0),
        (try_end),

        (try_for_range, ":troop_no", tavern_booksellers_begin, tavern_booksellers_end),
          (store_random_in_range, ":town_no", towns_begin, towns_end),
          (party_set_slot, ":town_no", slot_center_tavern_bookseller, ":troop_no"),
        (try_end),
    ]),
]
