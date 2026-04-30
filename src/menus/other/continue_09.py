MENUS = [
(
    "cut_siege_without_fight", mnf_enable_hot_keys,
    "The besiegers let you approach the gates without challenge.",
    "none",
    [
      (set_background_mesh, "mesh_pic_siege_join"),
#      (try_begin),
#        (troop_get_type, ":is_female", "trp_player"),
#        (eq, ":is_female", 1),
#        (set_background_mesh, "mesh_pic_siege_join_sighted_fem"),
#      (else_try),
#        (set_background_mesh, "mesh_pic_siege_join_sighted"),
#      (try_end),
    ],
    [
      ("continue", [], "Continue...", [(try_begin),
                                   (this_or_next|eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
                                   (eq, "$g_encountered_party_faction", "$players_kingdom"),
                                   (jump_to_menu, "mnu_town"),
                                 (else_try),
                                   (jump_to_menu, "mnu_castle_outside"),
                                 (try_end)]),
      ]
  ),
]
