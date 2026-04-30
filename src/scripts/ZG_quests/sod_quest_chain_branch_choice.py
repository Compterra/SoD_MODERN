SCRIPTS = [
("sod_quest_chain_branch_choice",
    [
      (store_script_param, ":quest_no", 1),
      (store_script_param, ":choice_id", 2),
      (store_script_param, ":next_quest", 3),
      (store_script_param, ":delay_days", 4),
      (quest_set_slot, ":quest_no", slot_quest_sod_chain_choice, ":choice_id"),
      (call_script, "script_sod_quest_chain_advance", ":quest_no", sod_quest_chain_branch_choice, ":next_quest", ":delay_days"),
  ]),
]
