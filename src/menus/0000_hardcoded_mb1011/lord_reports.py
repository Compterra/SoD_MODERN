MENUS = [
("lord_reports", mnf_enable_hot_keys,
    "{s98}",
    "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),

      (try_begin),
        (gt, "$players_kingdom", 0),
        (str_store_faction_name, s68, "$players_kingdom"),
        (faction_get_slot, ":King", "$players_kingdom", slot_faction_leader),
        (try_begin),
          (eq, ":King", "trp_player"),
          (str_store_string, s98, "@You are the {King/Queen} of the {s68}."),
        (else_try),
          (call_script, "script_store_troop_name", s69, ":King"),
          (try_begin),
            (eq, "$player_has_homage", 1),
            (str_store_string, s98, "@You serve {s69} of the {s68} as a vassal."),
          (else_try),
            (str_store_string, s98, "@You are contracted to the {s68}."),
          (try_end),
        (try_end),
      (else_try),
        (str_store_string, s98, "@You owe allegiance to no realm."),
      (try_end),
    ],
    [
#MORDACHAI - new lords relations report
      ("view_lord_relationship_report", [(gt, "$players_kingdom", 0)],
       "View lord relations report.",
       [(jump_to_menu, "mnu_lord_relations_report"), ]),

#MORDACHAI - new lords finances report
      ("view_lord_finances_report", [(gt, "$players_kingdom", 0)],
       "View lord finances report.",
       [(jump_to_menu, "mnu_lord_finances_report"), ]),

#MORDACHAI - new lords battle readiness report
      ("view_lord_readiness_report", [(gt, "$players_kingdom", 0)],
       "View lord battle readiness report.",
       [(jump_to_menu, "mnu_lord_readiness_report"), ]),

#MORDACHAI - new lords fief assignments report
      ("view_lord_fief_assignment_report", [(gt, "$players_kingdom", 0)],
       "View lord fief assignment report.",
       [(jump_to_menu, "mnu_lord_fief_assignment_report"), ]),

      ("view_lord_other", [], "Let me see a different report...", [(jump_to_menu, "mnu_reports")]),
      ("view_lord_travel", [], "Resume travelling.", [(change_screen_return)]),
    ]
  ),
]
