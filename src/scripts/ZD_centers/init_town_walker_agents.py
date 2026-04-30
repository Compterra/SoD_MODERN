SCRIPTS = [
("init_town_walker_agents",
      [(assign, ":num_walkers", 0),
        (try_for_agents, ":cur_agent"),
          (agent_get_troop_id, ":cur_troop", ":cur_agent"),
          (is_between, ":cur_troop", walkers_begin, walkers_end),
          (val_add, ":num_walkers", 1),
          (agent_get_position, pos1, ":cur_agent"),
          (try_for_range, ":i_e_p", 9, 40), #Entry points
            (entry_point_get_position, pos2, ":i_e_p"),
            (get_distance_between_positions, ":distance", pos1, pos2),
            (lt, ":distance", 200),
            (agent_set_slot, ":cur_agent", 0, ":i_e_p"),
          (try_end),
          (call_script, "script_set_town_walker_destination", ":cur_agent"),
        (try_end),
    ]),
]
