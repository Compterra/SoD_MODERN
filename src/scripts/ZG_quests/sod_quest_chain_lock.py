SCRIPTS = [
("sod_quest_chain_lock",
    [
      (store_script_param, ":quest_no", 1),
      (store_script_param, ":lock_state", 2),
      (quest_set_slot, ":quest_no", slot_quest_sod_chain_lock_state, ":lock_state"),
      (try_begin),
        (eq, ":lock_state", sod_quest_chain_lock_locked),
        (quest_get_slot, ":flags", ":quest_no", slot_quest_sod_chain_flags),
        (val_or, ":flags", sod_quest_chain_flag_lockout),
        (quest_set_slot, ":quest_no", slot_quest_sod_chain_flags, ":flags"),
        (quest_set_slot, ":quest_no", slot_quest_sod_runtime_state, sod_quest_state_locked),
      (try_end),
  ]),
]
