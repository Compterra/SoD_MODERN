MENUS = [
(
    "seven_ash_oath_council", mnf_disable_all_keys,
    "{s1}^^{s2}^^{s3}^^The council meets in the church because stone makes frightened people speak more quietly. A rough map of Ashwick lies across a trestle table: sightlines, ditches, gates, wells, cellars, and roads marked in different hands.",
    "none",
    [
      (set_background_mesh, "mesh_pic_village_w"),
      (quest_get_slot, ":recruited", "qst_seven_ash_ultimatum", slot_quest_seven_ash_recruited_bitmask),
      (quest_get_slot, ":resolved", "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_resolved_count),
      (assign, reg1, ":resolved"),
      (try_begin),
        (gt, ":recruited", 0),
        (str_store_string, s1, "@Recruited defenders mark what they understand: Garric draws patient sightlines; Oswin marks failure points in ditch and gate; Aldrik writes oath beside ranks; Mirelle pricks hidden doors and exits; Tomas numbers watches; Beren circles the breach with one hard thumb; Elianor writes water, wounded, shelter, and cellars. Missing roads leave blank places on the map. Resolved roads: {reg1}."),
      (else_try),
        (str_store_string, s1, "@No defender stands fully won at the table. Mother Hilda, Reeve Martin, Nell, and the player must choose without the seven voices Ashwick hoped for. Resolved roads: {reg1}."),
      (try_end),
      (try_begin),
        (store_and, ":bit", ":recruited", sod_seven_ash_defender_aldrik),
        (gt, ":bit", 0),
        (str_store_string, s2, "@Aldrik objects to dishonor: prisoners and frightened villagers cannot become props for a brave-looking plan. He supports lawful restraint and a public oath."),
      (else_try),
        (store_and, ":bit", ":recruited", sod_seven_ash_defender_mirelle),
        (gt, ":bit", 0),
        (str_store_string, s2, "@Mirelle supports dirty work only when it opens exits. She objects to any plan that turns fear into spectacle."),
      (else_try),
        (str_store_string, s2, "@Mother Hilda keeps one hand on the church key and asks who will still be alive to hear victory named."),
      (try_end),
      (try_begin),
        (store_and, ":bit", ":recruited", sod_seven_ash_defender_tomas),
        (gt, ":bit", 0),
        (str_store_string, s3, "@Tomas supports discipline with rules, not cruelty. Beren supports force with a named stop. Elianor supports any plan that counts wounded before pride."),
      (else_try),
        (store_and, ":bit", ":recruited", sod_seven_ash_defender_beren),
        (gt, ":bit", 0),
        (str_store_string, s3, "@Beren wants the breach named honestly and Halvorn answered there. He objects to pretending hunger and force are virtues by themselves."),
      (else_try),
        (str_store_string, s3, "@Nell's road marks make Wulfred sound practical, organized, and close: wagons, scouts, bought blades, and pressure before fire."),
      (try_end),
    ],
    [
      ("seven_ash_oath_council_begin", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act3_pressure_started, 1),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_final_plan, sod_seven_ash_plan_none),
      ], "Argue the map and choose Ashwick's oath.", [
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_oath_council),
        (start_map_conversation, "trp_seven_ash_mother_hilda"),
      ]),
      ("seven_ash_oath_council_back", [], "Return to Ashwick's preparations.", [
        (jump_to_menu, "mnu_seven_ash_pressure_board"),
      ]),
    ]
  ),
]

