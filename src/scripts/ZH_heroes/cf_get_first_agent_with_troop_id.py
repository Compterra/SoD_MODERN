SCRIPTS = [
("cf_get_first_agent_with_troop_id",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":result", -1),
      (try_for_agents, ":cur_agent"),
        (eq, ":result", -1),
        (agent_get_troop_id, ":cur_troop_no", ":cur_agent"),
        (eq, ":cur_troop_no", ":troop_no"),
        (assign, ":result", ":cur_agent"),
      (try_end),
      (assign, reg0, ":result"),
      (neq, reg0, -1),
  ]),
]
