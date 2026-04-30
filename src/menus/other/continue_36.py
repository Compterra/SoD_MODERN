MENUS = [
(
    "town_tournament_won_by_another", mnf_disable_all_keys,
    "As the only {reg3?fighter:man} to remain undefeated this day, {s1} wins the lists and the glory of this tournament.",
    "none",
    [ (assign, "$tournament_high_bet", 0), #twan456
      (call_script, "script_get_num_tournament_participants"),
      (store_sub, ":needed_to_remove_randomly", reg0, 1),
      (call_script, "script_remove_tournament_participants_randomly", ":needed_to_remove_randomly"),
      (call_script, "script_sort_tournament_participant_troops"),
      (troop_get_slot, ":winner_troop", "trp_tournament_participants", 0),
      (call_script, "script_store_troop_name", s1, ":winner_troop"),
      (try_begin),
        (troop_is_hero, ":winner_troop"),
        (call_script, "script_change_troop_renown", ":winner_troop", 20),
      (try_end),
      (troop_get_type, reg3, ":winner_troop"),
    ],
    [
      ("continue", [], "Continue...", [(jump_to_menu, "mnu_town")]),
    ]
  ),
]
