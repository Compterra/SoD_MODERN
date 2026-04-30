SCRIPTS = [
("sod_quest_chain_alternate_ending",
    [
      (store_script_param, ":quest_no", 1),
      (store_script_param, ":ending_id", 2),
      (quest_set_slot, ":quest_no", slot_quest_sod_chain_branch, sod_quest_chain_branch_alternate_ending),
      (quest_set_slot, ":quest_no", slot_quest_sod_chain_ending, ":ending_id"),
      (quest_set_slot, ":quest_no", slot_quest_sod_chain_lock_state, sod_quest_chain_lock_completed),
      (str_store_quest_name, s1, ":quest_no"),
      (display_message, "@Quest chain ending recorded: {s1}.", quest_success_color),
  ]),
]
