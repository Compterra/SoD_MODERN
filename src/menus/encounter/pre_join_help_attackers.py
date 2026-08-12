MENUS = [
(
    "pre_join", mnf_enable_hot_keys,
    "You come across a battle between:^^{s70} and {s73}.^^You decide to...",
    "none",
    [
      (set_background_mesh, "mesh_pic_involve"),

      (str_store_string, s70, "@an attacking force"),
      (try_begin),
        (gt, "$g_encountered_party_2", 0),
        (party_is_active, "$g_encountered_party_2"),
        (store_faction_of_party, ":attackers_faction", "$g_encountered_party_2"),
        (str_store_party_name, s68, "$g_encountered_party_2"),
        (str_store_faction_name, s69, ":attackers_faction"),
        (str_store_string, s70, "@{s68} of the {s69}"),
      (try_end),
      (str_store_string, s73, "@the defenders"),
      (try_begin),
        (gt, "$g_encountered_party", 0),
        (party_is_active, "$g_encountered_party"),
        (store_faction_of_party, ":defender_faction", "$g_encountered_party"),
        (str_store_party_name, s71, "$g_encountered_party"),
        (str_store_faction_name, s72, ":defender_faction"),
        (str_store_string, s73, "@{s71} of the {s72}"),
      (try_end),
    ],
    [
      ("pre_join_help_attackers",
      [
        (gt, "$g_encountered_party_2", 0),
        (party_is_active, "$g_encountered_party_2"),
        (gt, "$g_encountered_party", 0),
        (party_is_active, "$g_encountered_party"),
        (store_faction_of_party, ":attacker_faction", "$g_encountered_party_2"),
        # Use the player's current political allegiance. The supporters faction
        # only represents an independent player realm.
        (assign, ":player_faction", "fac_player_faction"),
        (try_begin),
          (gt, "$players_kingdom", 0),
          (assign, ":player_faction", "$players_kingdom"),
        (try_end),
        (store_relation, ":attacker_relation", ":attacker_faction", ":player_faction"),
        (ge, ":attacker_relation", 0),
      ],
      "Move in to help {s70}.", [
        (select_enemy, 0),
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", "$g_encountered_party_2"),
        (assign, "$g_sod_joined_ongoing_ai_battle", 1),
        (jump_to_menu, "mnu_join_battle")
      ]),

      ("pre_join_help_defenders",
      [
        (gt, "$g_encountered_party", 0),
        (party_is_active, "$g_encountered_party"),
        (gt, "$g_encountered_party_2", 0),
        (party_is_active, "$g_encountered_party_2"),
        (store_faction_of_party, ":defender_faction", "$g_encountered_party"),
        (assign, ":player_faction", "fac_player_faction"),
        (try_begin),
          (gt, "$players_kingdom", 0),
          (assign, ":player_faction", "$players_kingdom"),
        (try_end),
        (store_relation, ":defender_relation", ":defender_faction", ":player_faction"),
        (ge, ":defender_relation", 0),
      ],
      "Rush to the aid of {s73}.", [
        (select_enemy, 1),
        (assign, "$g_enemy_party", "$g_encountered_party_2"),
        (assign, "$g_ally_party", "$g_encountered_party"),
        (assign, "$g_sod_joined_ongoing_ai_battle", 1),
        (jump_to_menu, "mnu_join_battle")
      ]),

      ("pre_join_leave", [], "Don't get involved.", [(leave_encounter), (change_screen_return)]),
    ]
  ),
]
