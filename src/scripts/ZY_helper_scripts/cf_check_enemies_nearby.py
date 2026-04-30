SCRIPTS = [
("cf_check_enemies_nearby",
    [
      (get_player_agent_no, ":player_agent"),
      (agent_is_alive, ":player_agent"),
      (agent_get_position, pos1, ":player_agent"),
      (assign, ":result", 0),
      (set_fixed_point_multiplier, 100),
      (try_for_agents, ":cur_agent"),
        (neq, ":cur_agent", ":player_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (neg|agent_is_ally, ":cur_agent"),
        (agent_get_position, pos2, ":cur_agent"),
        (get_distance_between_positions, ":cur_distance", pos1, pos2),
        (le, ":cur_distance", 1500), #15 meters
        (assign, ":result", 1),
      (try_end),
      (eq, ":result", 0),
  ]),
]
