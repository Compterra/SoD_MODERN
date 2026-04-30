SCRIPTS = [
("recalculate_ai_for_troop",
    [
      (store_script_param, ":troop_no", 1),
      (call_script, "script_init_ai_calculation"),
      (call_script, "script_calculate_troop_ai", ":troop_no"),
      (call_script, "script_calculate_troop_ai_under_command", ":troop_no"),
  ]),
]
