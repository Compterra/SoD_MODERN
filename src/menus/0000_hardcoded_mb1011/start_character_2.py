MENUS = [
(
    "start_character_2", mnf_disable_all_keys,
    "{s10}^^How could the heavens allow such a thing? How could these evil pagans defeat those who share the true faith in...",
    "none",
    [
      (set_background_mesh, "mesh_pic_chr3_faith"),
    ],
    [
      ("the_one", [], "The One.", [
        (assign, "$background_answer_2", cb_the_one),
        (assign, reg3, "$character_gender"),
        (str_store_string, s11, "@As a {reg3?girl:boy} growing out of childhood, you were taught that the world is more than what can be touched. The Temple showed you the true path. There is a reason and purpose for all creation, and that reason and purpose is The One."),
        (jump_to_menu, "mnu_start_character_3"),
      ]),

      ("old_gods", [], "The Old Gods.", [
        (assign, "$background_answer_2", cb_old_gods),
        (assign, reg3, "$character_gender"),
        (str_store_string, s11, "@As a {reg3?girl:boy} growing out of childhood, you were taught to honor The Old Gods and your ancestors."),
        (jump_to_menu, "mnu_start_character_3"),
      ]),

      ("the_void", [], "The Void", [
        (assign, "$background_answer_2", cb_the_void),
        (assign, reg3, "$character_gender"),
        (str_store_string, s11, "@As a {reg3?girl:boy} growing out of childhood, you read the forbidden texts of the ancients. Soon, together with others like you, you found a path to The Void. Or perhaps it found you."),
        (jump_to_menu, "mnu_start_character_3"),
      ]),

      ("enlightenment", [], "Spiritual Enlightenment.", [
        (assign, "$background_answer_2", cb_enlightenment),
        (assign, reg3, "$character_gender"),
        (str_store_string, s11, "@As a {reg3?girl:boy} growing out of childhood, you were surrounded by others who prized self-discipline. You came to believe that the whole world is an illusion. There is only Now. Past, future, self, and other are all illusions. To awaken to reality became your driving focus."),
        (jump_to_menu, "mnu_start_character_3"),
      ]),

      ("atheism", [], "Natural Philosophy.", [
        (assign, "$background_answer_2", cb_atheism),
        (assign, reg3, "$character_gender"),
        (str_store_string, s11, "@As a {reg3?girl:boy} growing out of childhood, you were taught much about faith. But groveling before gods, pretending they may hear you or even that they exist, is beneath you. You make your own destiny!"),
        (jump_to_menu, "mnu_start_character_3"),
      ]),

      ("go_back", [], "Go back.", [
        (jump_to_menu, "mnu_start_character_1"),
      ]),
    ]
  ),
]
