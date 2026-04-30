SCRIPTS = [
("rally",
                      [
                        #(display_message, "@Your enemies rally to rejoin the battle!", red),
                        (try_for_agents, ":agent"),
                          (agent_is_alive, ":agent"),
                          (agent_is_human, ":agent"),
                          (store_agent_hit_points, ":hitpoints", ":agent", 0),
                          #(val_sub, ":hitpoints", 10),
                          (store_random_in_range, ":routed", 1, 101),
                          (try_begin),
                            (le, ":routed", ":hitpoints"),
                            (agent_clear_scripted_mode, ":agent"),
                          (try_end),
                        (end_try),
                      ]
                    ),
]
