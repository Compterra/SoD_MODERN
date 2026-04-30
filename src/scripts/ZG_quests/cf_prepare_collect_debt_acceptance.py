SCRIPTS = [
("cf_prepare_collect_debt_acceptance",
    [
      (store_script_param, ":quest_no", 1),
      (store_script_param, ":talk_troop", 2),

      (this_or_next|eq, ":quest_no", "qst_collect_debt"),
      (this_or_next|eq, ":quest_no", "qst_conquistadors_collect_debt"),
      (this_or_next|eq, ":quest_no", "qst_black_army_collect_debt"),
      (eq, ":quest_no", "qst_slavers_collect_debt"),

      (check_quest_active, ":quest_no"),
      (quest_slot_eq, ":quest_no", slot_quest_current_state, 0),
      (quest_slot_eq, ":quest_no", slot_quest_target_troop, ":talk_troop"),
      (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
      (call_script, "script_store_troop_name", s8, ":quest_giver_troop"),
      (quest_get_slot, reg10, ":quest_no", slot_quest_target_amount),
    ]),
]
