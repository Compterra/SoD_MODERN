SCRIPTS = [
("cf_troop_agent_is_alive",
        [(store_script_param, ":troop_no", 1),
          (assign, ":alive_count", 0),
          (try_for_agents, ":cur_agent"),
            (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
            (eq, ":troop_no", ":cur_agent_troop"),
            (agent_is_alive, ":cur_agent"),
            (val_add, ":alive_count", 1),
          (try_end),
          (gt, ":alive_count", 0),
      ]),
]
