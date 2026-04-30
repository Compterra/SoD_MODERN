DIALOGS = [
[trp_sod_chancellor|plyr, "chancellor_lord_action",  [(ge, "$lords", 1), (ge, "$territory", 1)], "Recruit new lord.", "chancellor_lord_recruited",
    [
      # choose a lord at random
      (store_random_in_range, ":roll", 0, "$lords"),
      (troop_get_slot, ":lord", "trp_temp_array_a", ":roll"),

      # intitialize the new lord to be in the player's kingdom with a banner, etc.
      (troop_set_slot, ":lord", slot_troop_change_to_faction, "fac_player_supporters_faction"),
      (troop_set_slot, ":lord", slot_troop_occupation, slto_kingdom_hero),
      (troop_set_slot, ":lord", slot_troop_wealth, recruited_lord_starting_funds),
      # (troop_get_slot, ":selected_banner_spr", "trp_player", slot_troop_banner_scene_prop),
      # (troop_set_slot, ":lord", slot_troop_banner_scene_prop, ":selected_banner_spr"),
      (troop_set_slot, ":lord", slot_troop_original_faction, "fac_player_supporters_faction"),

      # give them an initial relation of 0..10
      (store_random_in_range, ":relation", 0, 11),
      (troop_set_slot, ":lord", slot_troop_player_relation, ":relation"),

      # generate a string to indicate who's joining us
      (call_script, "script_store_troop_name_link", s1, ":lord"),
      (str_store_string, s1, "@{s1} shall be granted titles and honors befitting a Lord."),
    ]
  ],
]
