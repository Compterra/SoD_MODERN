MENUS = [
(
    "start_character_4", mnf_disable_all_keys,
    "{s12}^^But I have not spoken my last word. One day I will return and...",
    #Finally, what made you decide to strike out on your own as an adventurer?",
    "none",
    [
      (set_background_mesh, "mesh_pic_chr5_future"),
    ],
    [
      ("revenge", [], "Will have my revenge.", [
        (assign, "$background_answer_4", cb4_revenge),
        (str_store_string, s13, "@You want vengeance. You want justice. What was done to you cannot be undone, and these debts can only be paid in blood..."),
        (jump_to_menu, "mnu_choose_skill"),
        ]),
      ("death", [], "Bring peace to the people of my country.", [
        (assign, "$background_answer_4", cb4_peace),
        (str_store_string, s13, "@Oppression cannot last forever. You will build an army strong enough to free your people!"),
        (jump_to_menu, "mnu_choose_skill"),
        ]),
      ("wanderlust", [], "Fight! I just love war!", [
        (assign, "$background_answer_4", cb4_bloodlust),
        (str_store_string, s13, "@War is all that matters. It reveals all that is best and worst in humans."),
        (jump_to_menu, "mnu_choose_skill"),
        ]),
      ("disown", [], "Reclaim my wealth.", [
        (assign, "$background_answer_4", cb4_riches),
        (str_store_string, s13, "@I just want a peaceful, easy life. This is the life I lost..."),
        (jump_to_menu, "mnu_choose_skill"),
        ]),
      ("go_back", [], "Go back.",
       [(jump_to_menu, "mnu_start_character_3"),
        ]
       ),
    ]
  ),
]
