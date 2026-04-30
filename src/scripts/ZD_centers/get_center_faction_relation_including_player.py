SCRIPTS = [
("get_center_faction_relation_including_player",
    [
      (store_script_param, ":center_no", 1),
      (store_script_param, ":target_faction_no", 2),
      (store_faction_of_party, ":center_faction", ":center_no"),
      (store_relation, ":reln", ":center_faction", ":target_faction_no"),
      (try_begin),
        (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (store_relation, ":reln", "fac_player_supporters_faction", ":target_faction_no"),
      (try_end),
      (assign, reg0, ":reln"),
  ]),
]
