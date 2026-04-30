SCRIPTS = [
("set_parties_around_player_ignore_player",
        [(store_script_param, ":ignore_range", 1),
          (store_script_param, ":num_hours", 2),
          (try_for_parties, ":party_no"),
            (party_is_active, ":party_no"),
            (store_distance_to_party_from_party, ":dist", "p_main_party", ":party_no"),
            (lt, ":dist", ":ignore_range"),
            (party_ignore_player, ":party_no", ":num_hours"),
          (try_end),
      ]),
]
