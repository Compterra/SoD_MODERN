SCRIPTS = [
("sod_quest_chain_apply_outcome",
    [
      (store_script_param, ":quest_no", 1),
      (store_script_param, ":outcome_branch", 2),
      (quest_get_slot, ":next_quest", ":quest_no", slot_quest_sod_chain_next_quest),
      (try_begin),
        (is_between, ":next_quest", all_quests_begin, all_quests_end),
        (quest_get_slot, ":branch_type", ":quest_no", slot_quest_sod_chain_branch),
        (this_or_next|eq, ":branch_type", sod_quest_chain_branch_none),
        (eq, ":branch_type", ":outcome_branch"),
        (call_script, "script_sod_quest_chain_advance", ":quest_no", ":outcome_branch", ":next_quest", 0),
      (else_try),
        (eq, ":outcome_branch", sod_quest_chain_branch_success),
        (quest_slot_eq, ":quest_no", slot_quest_sod_chain_lock_state, sod_quest_chain_lock_none),
        (quest_set_slot, ":quest_no", slot_quest_sod_chain_lock_state, sod_quest_chain_lock_completed),
        (quest_set_slot, ":quest_no", slot_quest_sod_chain_ending, sod_quest_chain_branch_success),
      (else_try),
        (eq, ":outcome_branch", sod_quest_chain_branch_failure),
        (quest_slot_eq, ":quest_no", slot_quest_sod_chain_lock_state, sod_quest_chain_lock_none),
        (quest_set_slot, ":quest_no", slot_quest_sod_chain_lock_state, sod_quest_chain_lock_failed),
        (quest_set_slot, ":quest_no", slot_quest_sod_chain_ending, sod_quest_chain_branch_failure),
      (try_end),
  ]),
]

script_sod_quest_chain_apply_outcome = SCRIPTS[0][1]
SCRIPT = script_sod_quest_chain_apply_outcome