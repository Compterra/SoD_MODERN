SCRIPTS = [
("count_parties_of_faction_and_party_type",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":party_type"),
      (assign, reg0, 0),
      (try_for_parties, ":party_no"),
        (party_is_active, ":party_no"),
        (party_get_slot, ":cur_party_type", ":party_no", slot_party_type),
        (store_faction_of_party, ":cur_faction", ":party_no"),
        (eq, ":cur_party_type", ":party_type"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, reg0, 1),
      (try_end),
  ]),
]
