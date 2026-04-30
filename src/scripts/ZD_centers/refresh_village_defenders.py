SCRIPTS = [
("refresh_village_defenders",
    [
      (store_script_param_1, ":village_no"),

      (assign, ":ideal_size", 50),
      (try_begin),
        (party_get_num_companions, ":size_before", ":village_no"),
        (lt, ":size_before", ":ideal_size"),
        (party_get_slot, ":pop", ":village_no", slot_center_sod_local_population),
        (store_sub, ":surplus", ":pop", village_pop_min),
        (val_max, ":surplus", 0),
        (party_add_template, ":village_no", "pt_village_defenders"),
        (party_get_num_companions, ":size_after", ":village_no"),
        (store_sub, ":added", ":size_after", ":size_before"),
        (val_min, ":added", ":surplus"),
        (val_sub, ":pop", ":added"),
        (val_max, ":pop", village_pop_min),
        (party_set_slot, ":village_no", slot_center_sod_local_population, ":pop"),
      (try_end),
  ]),
]
