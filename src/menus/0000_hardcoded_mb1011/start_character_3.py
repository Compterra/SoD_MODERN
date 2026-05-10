MENUS = [
(
    "start_character_3", mnf_disable_all_keys,
    "{s11}^^ As you leave the burned land you also leave your old life of...",
    "none",
    [
      (set_background_mesh, "mesh_pic_chr4_past"),
      (assign, reg3, "$character_gender"),
    ],
    [
      ("squire", [], "Tournaments and duels.", [
        (assign, "$background_answer_3", cb3_tourneys),
        (str_store_string, s14, "@{reg3?daughter:man}"),
        (str_store_string, s12, "@You were spending your adult life searching an occasion to practice your weapon skills."),
        (jump_to_menu, "mnu_start_character_4"),
        ]),
      ("troubadour", [], "Intrigues.", [
        (assign, "$background_answer_3", cb3_intrigues),
        (str_store_string, s14, "@{reg3?daughter:man}"),
        (str_store_string, s13, "@{reg3?woman:man}"),
        (str_store_string, s12, "@You were spending your adult life in the dirty world of politics."),
        (jump_to_menu, "mnu_start_character_4"),
        ]),
      ("student", [], "Philosophy.", [
        (assign, "$background_answer_3", cb3_philosophy),
        (str_store_string, s12, "@You were spending your adult life studying philosophy."),
        (jump_to_menu, "mnu_start_character_4"),
        ]),
      ("peddler", [], "Trade.", [
        (assign, "$background_answer_3", cb3_merchant),
        (str_store_string, s14, "@{reg3?daughter:man}"),
        (str_store_string, s13, "@{reg3?woman:man}"),
        (str_store_string, s12, "@You were spending your adult life building your own trading empire."),
        (jump_to_menu, "mnu_start_character_4"),
        ]),
      ("go_back", [], "Go back.",
       [(jump_to_menu, "mnu_start_character_2"),
        ]
       ),
    ]
  ),
]
