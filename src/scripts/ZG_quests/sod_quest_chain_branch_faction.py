SCRIPTS = [
("sod_quest_chain_branch_faction",
    [
      (store_script_param, ":quest_no", 1),
      (store_script_param, ":faction_no", 2),
      (store_script_param, ":aligned_next_quest", 3),
      (store_script_param, ":opposed_next_quest", 4),
      (store_script_param, ":delay_days", 5),
      (store_relation, ":relation", "fac_player_supporters_faction", ":faction_no"),
      (try_begin),
        (ge, ":relation", 0),
        (call_script, "script_sod_quest_chain_advance", ":quest_no", sod_quest_chain_branch_faction, ":aligned_next_quest", ":delay_days"),
      (else_try),
        (call_script, "script_sod_quest_chain_advance", ":quest_no", sod_quest_chain_branch_faction, ":opposed_next_quest", ":delay_days"),
      (try_end),
  ]),
]
