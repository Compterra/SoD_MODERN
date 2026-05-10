DIALOGS = [
[trp_slave_hero, "start", [
  (eq, "$prison_break", 2),
  (check_quest_active, "qst_slave_q2"),
  (neg|check_quest_active, "qst_slave_q3"),
  (neg|check_quest_succeeded, "qst_slave_q3"),
  (neg|check_quest_failed, "qst_slave_q3"),
  (assign, "$prison_break", -1),
  (str_store_troop_name, s13, "$prison_break_random_lord"),
  ], "You made it back. Tell me plainly: did {s13} remember the old debt, or only the danger?", "prison_break_2_1", []],
]
