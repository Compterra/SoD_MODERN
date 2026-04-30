SCRIPTS = [
("update_tavern_minstels",
      [(try_for_range, ":town_no", towns_begin, towns_end),
          (party_set_slot, ":town_no", slot_center_tavern_minstrel, 0),
        (try_end),

        (try_for_range, ":troop_no", tavern_minstrels_begin, tavern_minstrels_end),
          (store_random_in_range, ":town_no", towns_begin, towns_end),
          (party_set_slot, ":town_no", slot_center_tavern_minstrel, ":troop_no"),
        (try_end),
    ]),
]
