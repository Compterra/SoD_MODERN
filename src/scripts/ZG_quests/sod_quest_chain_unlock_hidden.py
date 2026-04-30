SCRIPTS = [
("sod_quest_chain_unlock_hidden",
    [
      (store_script_param, ":quest_no", 1),
      (store_script_param, ":next_quest", 2),
      (quest_get_slot, ":flags", ":quest_no", slot_quest_sod_chain_flags),
      (val_or, ":flags", sod_quest_chain_flag_hidden_unlocked),
      (quest_set_slot, ":quest_no", slot_quest_sod_chain_flags, ":flags"),
      (quest_set_slot, ":quest_no", slot_quest_sod_chain_branch, sod_quest_chain_branch_hidden),
      (quest_set_slot, ":quest_no", slot_quest_sod_chain_next_quest, ":next_quest"),
      (quest_set_slot, ":quest_no", slot_quest_sod_runtime_state, sod_quest_state_revealed),
      (str_store_quest_name, s1, ":quest_no"),
      (display_message, "@Hidden quest path revealed: {s1}.", quest_success_color),
  ]),
]
