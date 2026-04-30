DIALOGS = [
[trp_slave_hero, "start", [
  (eq, "$prison_break", 2),
  (assign, "$prison_break", -1),
  (str_store_troop_name, s13, "$prison_break_random_lord"),
  ], "Ah, you're back! So, what did {s13} say?", "prison_break_2_1", []],
]
