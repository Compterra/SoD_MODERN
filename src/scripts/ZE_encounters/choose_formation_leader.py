SCRIPTS = [
("choose_formation_leader",
                      [
                        (assign, reg2, -1),
                        (assign, ":max_xp", 0),
                        (try_for_agents, ":agent"),
                          (agent_is_alive, ":agent"),
                          (agent_is_human, ":agent"),
                          (agent_get_team, ":team", ":agent"),
                          (eq, ":team", reg0),
                          (agent_get_class, ":class", ":agent"),
                          (eq, ":class", reg1),
                          (get_player_agent_no, ":player"),
                          (neq, ":player", ":agent"),
                          (agent_get_troop_id, ":troop", ":agent"),
                          (troop_get_xp, ":xp", ":troop"),
                          (gt, ":xp", ":max_xp"),
                          (assign, ":max_xp", ":xp"),
                          (assign, reg2, ":agent"),
                        (end_try),
                      ]
                    ),
]
