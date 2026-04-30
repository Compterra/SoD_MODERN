MENUS = [
(
    "join_siege_outside", mnf_enable_hot_keys, #mnf_scale_picture|
    "{s1} has come under siege by {s2}.",
    "none",
    [
      (set_background_mesh, "mesh_pic_siege_join"),
      (str_store_party_name, s1, "$g_encountered_party"),
      (str_store_party_name, s2, "$g_encountered_party_2"),
#      (troop_get_type, ":is_female", "trp_player"),
#      (try_begin),
#        (eq, ":is_female", 1),
#        (set_background_mesh, "mesh_pic_siege_join_sighted_fem"),
#      (else_try),
#        (set_background_mesh, "mesh_pic_siege_join_sighted"),
#      (try_end),
    ],
    [
      ("approach_besiegers", [(store_faction_of_party, ":faction_no", "$g_encountered_party_2"),
                             (store_relation, ":relation", ":faction_no", "fac_player_supporters_faction"),
                             (ge, ":relation", 0),
                             (store_faction_of_party, ":faction_no", "$g_encountered_party"),
                             (store_relation, ":relation", ":faction_no", "fac_player_supporters_faction"),
                             (lt, ":relation", 0),
                             ], "Approach the siege camp.", [
          (jump_to_menu, "mnu_besiegers_camp_with_allies"),
                                ]),
      ("pass_through_siege", [(store_faction_of_party, ":faction_no", "$g_encountered_party"),
                             (store_relation, ":relation", ":faction_no", "fac_player_supporters_faction"),
                             (ge, ":relation", 0),
                             ], "Pass through the siege lines and enter {s1}.",
       [
            (jump_to_menu, "mnu_cut_siege_without_fight"),
          ]),
      ("leave", [], "Leave.", [(leave_encounter),
                            (change_screen_return)]),
    ]
  ),
]
