SCRIPTS = [
("battle_tactic_apply",
    [
      (call_script, "script_battle_tactic_apply_aux", "$ai_team_1", "$ai_team_1_battle_tactic"),
      (assign, "$ai_team_1_battle_tactic", reg0),
      (try_begin),
        (ge, "$ai_team_2", 0),
        (call_script, "script_battle_tactic_apply_aux", "$ai_team_2", "$ai_team_2_battle_tactic"),
        (assign, "$ai_team_2_battle_tactic", reg0),
      (try_end),
  ]),
]
