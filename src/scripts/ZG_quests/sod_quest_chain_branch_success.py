SCRIPTS = [
("sod_quest_chain_branch_success",
    [
      (store_script_param, ":quest_no", 1),
      (store_script_param, ":next_quest", 2),
      (store_script_param, ":delay_days", 3),
      (call_script, "script_sod_quest_chain_advance", ":quest_no", sod_quest_chain_branch_success, ":next_quest", ":delay_days"),
  ]),
]
