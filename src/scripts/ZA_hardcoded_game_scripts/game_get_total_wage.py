SCRIPTS = [
("game_get_total_wage",
    [
      (call_script, "script_calculate_player_faction_wage"),
      (assign, ":total_wages", reg0),
      (assign, reg6, ":total_wages"),
      (set_trigger_result, reg0),
  ]),
]
