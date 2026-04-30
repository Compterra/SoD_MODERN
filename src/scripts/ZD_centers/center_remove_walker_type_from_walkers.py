SCRIPTS = [
("center_remove_walker_type_from_walkers",
    [
      (store_script_param, ":center_no", 1),
      (store_script_param, ":walker_type", 2),
      (try_for_range, ":walker_no", 0, num_town_walkers),
        (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
        (party_slot_eq, ":center_no", ":type_slot", ":walker_type"),
        (call_script, "script_center_set_walker_to_type", ":center_no", ":walker_no", walkert_default),
      (try_end),
  ]),
]
