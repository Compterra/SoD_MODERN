SCRIPTS = [
("formation_end",
                      [
                        (try_for_agents, reg(5)),
                          (agent_is_alive, reg(5)),
                          (agent_is_human, reg(5)),
                          (agent_get_team  , ":team", reg5),
                          (eq, ":team", reg0),
                          (agent_get_class , ":class", reg5),
                          (eq, ":class", reg1),
                          (agent_clear_scripted_mode, reg5),
                        (try_end),
                      ]
                    ),
]
