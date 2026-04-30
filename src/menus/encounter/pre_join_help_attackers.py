MENUS = [
(
    "pre_join", mnf_enable_hot_keys,
    "You come across a battle between:^^{s2} and {s1}.^^You decide to...",
    "none",
    [
      (set_background_mesh, "mesh_pic_involve"),

      (store_faction_of_party, ":attackers_faction", "$g_encountered_party_2"),
      (store_faction_of_party, ":defender_faction", "$g_encountered_party"),
      (str_store_party_name, s2, "$g_encountered_party_2"),
      (str_store_faction_name, s4, ":attackers_faction"),
      (str_store_string, s2, "@{s2} of the {s4}"),
      (str_store_party_name, s1, "$g_encountered_party"),
      (str_store_faction_name, s3, ":defender_faction"),
      (str_store_string, s1, "@{s1} of the {s3}"),
    ],
    [
      ("pre_join_help_attackers",
      [
        (store_faction_of_party, ":attacker_faction", "$g_encountered_party_2"),
        (store_relation, ":attacker_relation", ":attacker_faction", "fac_player_supporters_faction"),
        (ge, ":attacker_relation", 0),

        # MORDACHAI - allow players to join in on neutral battles
        #(store_faction_of_party, ":defender_faction", "$g_encountered_party"),
        #(store_relation, ":defender_relation", ":defender_faction", "fac_player_supporters_faction"),
        #(lt, ":defender_relation", 0),
      ],
      "Move in to help {s2}.", [
        (select_enemy, 0),
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", "$g_encountered_party_2"),
        (jump_to_menu, "mnu_join_battle")
      ]),

      ("pre_join_help_defenders",
      [
        (store_faction_of_party, ":defender_faction", "$g_encountered_party"),
        (store_relation, ":defender_relation", ":defender_faction", "fac_player_supporters_faction"),
        (ge, ":defender_relation", 0),

        # MORDACHAI - allow players to join in on neutral battles
        #(store_faction_of_party, ":attacker_faction", "$g_encountered_party_2"),
        #(store_relation, ":attacker_relation", ":attacker_faction", "fac_player_supporters_faction"),
        #(lt, ":attacker_relation", 0),
      ],
      "Rush to the aid of {s1}.", [
        (select_enemy, 1),
        (assign, "$g_enemy_party", "$g_encountered_party_2"),
        (assign, "$g_ally_party", "$g_encountered_party"),
        (jump_to_menu, "mnu_join_battle")
      ]),

      ("pre_join_leave", [], "Don't get involved.", [(leave_encounter), (change_screen_return)]),
    ]
  ),
]
