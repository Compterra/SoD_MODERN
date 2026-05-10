MENUS = [
(
    "seven_ash_recruitment_map", mnf_disable_all_keys,
    "{s1}^^{s2}^^{s3}^^{s4}^^The board names roads, witnesses, and unfinished promises. No mark on it wins a defender; the road only tells you where the next conversation waits.",
    "none",
    [
      (set_background_mesh, "mesh_pic_siege_sighted"),
      (quest_get_slot, ":board_open", "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_board_open),
      (quest_get_slot, ":resolved", "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_resolved_count),
      (quest_get_slot, ":days", "qst_seven_ash_ultimatum", slot_quest_seven_ash_days_remaining),
      (quest_get_slot, ":garric_status", "qst_seven_ash_ultimatum", slot_quest_seven_ash_garric_status),
      (quest_get_slot, ":oswin_status", "qst_seven_ash_ultimatum", slot_quest_seven_ash_oswin_status),
      (quest_get_slot, ":aldrik_status", "qst_seven_ash_ultimatum", slot_quest_seven_ash_aldrik_status),
      (quest_get_slot, ":mirelle_status", "qst_seven_ash_ultimatum", slot_quest_seven_ash_mirelle_status),
      (quest_get_slot, ":tomas_status", "qst_seven_ash_ultimatum", slot_quest_seven_ash_tomas_status),
      (quest_get_slot, ":beren_status", "qst_seven_ash_ultimatum", slot_quest_seven_ash_beren_status),
      (quest_get_slot, ":elianor_status", "qst_seven_ash_ultimatum", slot_quest_seven_ash_elianor_status),
      (assign, reg1, ":resolved"),
      (assign, reg9, ":days"),
      (try_begin),
        (eq, ":board_open", 1),
        (assign, reg2, ":garric_status"),
        (assign, reg3, ":oswin_status"),
        (assign, reg4, ":aldrik_status"),
        (assign, reg5, ":mirelle_status"),
        (assign, reg6, ":tomas_status"),
        (assign, reg7, ":beren_status"),
        (assign, reg8, ":elianor_status"),
        (str_store_string, s1, "@The search is open. Days before emergency return: {reg9}. Roads answered: {reg1}/7."),
        (str_store_string, s2, "@Travel targets: Garric at the Split Hart tavern; Oswin at Harrowcut Quarry; Aldrik on Saint Cuthbert's chapel road; Mirelle at the Low Lantern; Tomas at the Red Crutch almshouse; Beren at the mill-yard pit; Elianor at Saint Ormond's refugee camp."),
        (str_store_string, s3, "@Road tallies: Garric {reg2}, Oswin {reg3}, Aldrik {reg4}, Mirelle {reg5}, Tomas {reg6}, Beren {reg7}, Elianor {reg8}."),
        (str_store_string, s4, "@Marks: 1 lead open, 2 road begun, 3 won, 4 refused, 5 present but bitter, 6 lost, 7 abandoned. Won or bitter defenders still need their Ashwick return before their craft is fully counted."),
      (else_try),
        (str_store_string, s1, "@Ashwick is preparing without a search board for now. Its next pressure will come at home, not down these roads."),
        (str_store_string, s2, "@No defender travel targets are active."),
        (str_store_string, s3, "@The road tallies are covered until the search begins."),
        (str_store_string, s4, "@The village will not face Wulfred's final pressure until the oaths and returns are settled."),
      (try_end),
    ],
    [
      ("seven_ash_board_garric", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_board_open, 1),
        (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_garric_status, sod_seven_ash_recruit_available),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_garric_status, sod_seven_ash_recruit_in_progress),
      ], "Ride to the Split Hart and find Garric Ashbow.", [
        (call_script, "script_sod_seven_ash_begin_defender_road", sod_seven_ash_defender_garric),
        (jump_to_menu, "mnu_seven_ash_garric_split_hart"),
      ]),
      ("seven_ash_board_oswin", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_board_open, 1),
        (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_oswin_status, sod_seven_ash_recruit_available),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_oswin_status, sod_seven_ash_recruit_in_progress),
      ], "Ride to Harrowcut Quarry and find Oswin Ditchwright.", [
        (call_script, "script_sod_seven_ash_begin_defender_road", sod_seven_ash_defender_oswin),
        (jump_to_menu, "mnu_seven_ash_oswin_quarry"),
      ]),
      ("seven_ash_board_aldrik", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_board_open, 1),
        (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_aldrik_status, sod_seven_ash_recruit_available),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_aldrik_status, sod_seven_ash_recruit_in_progress),
      ], "Ride to Saint Cuthbert's chapel road and find Sir Aldrik Vane.", [
        (call_script, "script_sod_seven_ash_begin_defender_road", sod_seven_ash_defender_aldrik),
        (jump_to_menu, "mnu_seven_ash_aldrik_chapel"),
      ]),
      ("seven_ash_board_mirelle", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_board_open, 1),
        (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_mirelle_status, sod_seven_ash_recruit_available),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_mirelle_status, sod_seven_ash_recruit_in_progress),
      ], "Ride to the Low Lantern and find Mirelle Voss.", [
        (call_script, "script_sod_seven_ash_begin_defender_road", sod_seven_ash_defender_mirelle),
        (jump_to_menu, "mnu_seven_ash_mirelle_low_lantern"),
      ]),
      ("seven_ash_board_tomas", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_board_open, 1),
        (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_tomas_status, sod_seven_ash_recruit_available),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_tomas_status, sod_seven_ash_recruit_in_progress),
      ], "Ride to the Red Crutch almshouse and find Tomas Reed.", [
        (call_script, "script_sod_seven_ash_begin_defender_road", sod_seven_ash_defender_tomas),
        (jump_to_menu, "mnu_seven_ash_tomas_almshouse"),
      ]),
      ("seven_ash_board_beren", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_board_open, 1),
        (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_beren_status, sod_seven_ash_recruit_available),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_beren_status, sod_seven_ash_recruit_in_progress),
      ], "Ride to the mill-yard pit and find Beren Hardhand.", [
        (call_script, "script_sod_seven_ash_begin_defender_road", sod_seven_ash_defender_beren),
        (jump_to_menu, "mnu_seven_ash_beren_pit"),
      ]),
      ("seven_ash_board_elianor", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_board_open, 1),
        (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_elianor_status, sod_seven_ash_recruit_available),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_elianor_status, sod_seven_ash_recruit_in_progress),
      ], "Ride to Saint Ormond's refugee camp and find Sister Elianor.", [
        (call_script, "script_sod_seven_ash_begin_defender_road", sod_seven_ash_defender_elianor),
        (jump_to_menu, "mnu_seven_ash_elianor_refugee_camp"),
      ]),
      ("seven_ash_board_garric_return", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_garric_return_applied, 0),
        (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_garric_status, sod_seven_ash_recruit_recruited),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_garric_status, sod_seven_ash_recruit_alienated),
      ], "Return with Garric to Ashwick's watch platform.", [
        (jump_to_menu, "mnu_seven_ash_garric_watch_platform"),
      ]),
      ("seven_ash_board_oswin_return", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_oswin_return_applied, 0),
        (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_oswin_status, sod_seven_ash_recruit_recruited),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_oswin_status, sod_seven_ash_recruit_alienated),
      ], "Return with Oswin to Ashwick's palisade.", [
        (jump_to_menu, "mnu_seven_ash_oswin_palisade"),
      ]),
      ("seven_ash_board_aldrik_return", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_aldrik_return_applied, 0),
        (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_aldrik_status, sod_seven_ash_recruit_recruited),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_aldrik_status, sod_seven_ash_recruit_alienated),
      ], "Return with Aldrik to Ashwick's gate.", [
        (jump_to_menu, "mnu_seven_ash_aldrik_gate"),
      ]),
      ("seven_ash_board_mirelle_return", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_mirelle_return_applied, 0),
        (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_mirelle_status, sod_seven_ash_recruit_recruited),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_mirelle_status, sod_seven_ash_recruit_alienated),
      ], "Return with Mirelle to Ashwick's hidden routes.", [
        (jump_to_menu, "mnu_seven_ash_mirelle_evacuation_routes"),
      ]),
      ("seven_ash_board_tomas_return", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_tomas_return_applied, 0),
        (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_tomas_status, sod_seven_ash_recruit_recruited),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_tomas_status, sod_seven_ash_recruit_alienated),
      ], "Return with Tomas to Ashwick's militia yard.", [
        (jump_to_menu, "mnu_seven_ash_tomas_militia_yard"),
      ]),
      ("seven_ash_board_beren_return", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_beren_return_applied, 0),
        (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_beren_status, sod_seven_ash_recruit_recruited),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_beren_status, sod_seven_ash_recruit_alienated),
      ], "Return with Beren to Ashwick's gate.", [
        (jump_to_menu, "mnu_seven_ash_beren_gate"),
      ]),
      ("seven_ash_board_elianor_return", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_elianor_return_applied, 0),
        (this_or_next|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_elianor_status, sod_seven_ash_recruit_recruited),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_elianor_status, sod_seven_ash_recruit_alienated),
      ], "Return with Elianor to Ashwick's church.", [
        (jump_to_menu, "mnu_seven_ash_elianor_infirmary"),
      ]),
      ("seven_ash_board_end_recruitment", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_board_open, 1),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_complete, 0),
        (quest_get_slot, ":resolved", "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_resolved_count),
        (ge, ":resolved", 3),
      ], "End the search and return to Ashwick.", [
        (jump_to_menu, "mnu_seven_ash_end_recruitment_confirm"),
      ]),
      ("seven_ash_board_return_to_ashwick", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_complete, 1),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act3_pressure_started, 0),
      ], "Return to Ashwick and face the village.", [
        (jump_to_menu, "mnu_seven_ash_return_to_ashwick"),
      ]),
      ("seven_ash_board_continue", [], "Leave the board for now.", [
        (jump_to_menu, "mnu_start_phase_2"),
      ]),
    ]
  ),
]

