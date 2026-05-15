SCRIPTS = [
("cf_training_ground_sub_routine_1_for_melee_details",
    [
      (store_script_param, ":value", 1),
      (ge, "$temp_3", ":value"),
      (val_add, ":value", 1),
      (troop_get_slot, ":troop_id", "trp_stack_selection_ids", ":value"),
      (call_script, "script_store_troop_name_link", s68, ":troop_id"),
  ]),
]
