SCRIPTS = [
("get_number_of_unclaimed_centers_by_player",
    [
      (assign, ":unclaimed_centers", 0),
      (assign, reg1, -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":faction_no", ":center_no"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (party_slot_eq, ":center_no", slot_town_claimed_by_player, 0),
        (party_get_num_companion_stacks, ":num_stacks", ":center_no"),
        (ge, ":num_stacks", 1), #castle is garrisoned
        (assign, reg1, ":center_no"),
        (val_add, ":unclaimed_centers", 1),
      (try_end),
      (assign, reg0, ":unclaimed_centers"),
  ]),
]
