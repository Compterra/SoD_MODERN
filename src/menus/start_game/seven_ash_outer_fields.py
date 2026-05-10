MENUS = [
(
    "seven_ash_outer_fields", mnf_disable_all_keys,
    "The outer fields are not a wall. They are hayricks, ditches, orchard rows, and farm tracks where the first fires will either be smothered or carried home. Nell's count marks {reg0} attackers in {reg1} pushes before the palisade takes the real weight.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (call_script, "script_sod_seven_ash_prepare_outer_fields"),
    ],
    [
      ("seven_ash_outer_fields_fight", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_siege_phase_active, sod_seven_ash_siege_phase_outer_fields),
      ], "Ride the ditch lanes and fight the first push.", [
        (modify_visitors_at_site, "scn_random_scene"),
        (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (set_visitor, 1, "trp_seven_ash_garric_ashbow"),
        (set_visitor, 2, "trp_seven_ash_tomas_reed"),
        (set_visitor, 3, "trp_watchman"),
        (set_visitor, 4, "trp_farmer"),
        (set_visitor, 10, "trp_bandit"),
        (set_visitor, 11, "trp_brigand"),
        (set_visitor, 12, "trp_henchman"),
        (set_visitor, 13, "trp_looter"),
        (set_visitor, 14, "trp_bandit"),
        (set_visitor, 15, "trp_seven_ash_sibert_crow_eye"),
        (set_jump_mission, "mt_seven_ash_outer_fields"),
        (jump_to_scene, "scn_random_scene"),
        (change_screen_mission),
      ]),
      ("seven_ash_outer_fields_fallback", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_siege_phase_active, sod_seven_ash_siege_phase_outer_fields),
      ], "Yield the fields and pull everyone behind the ditch.", [
        (call_script, "script_sod_seven_ash_resolve_outer_fields", sod_seven_ash_siege_result_lost),
        (jump_to_menu, "mnu_seven_ash_palisade_staging"),
      ]),
      ("seven_ash_outer_fields_back", [], "Return to Nell's report.", [
        (jump_to_menu, "mnu_seven_ash_siege_warning"),
      ]),
    ]
  ),

(
    "seven_ash_outer_fields_held", mnf_disable_all_keys,
    "The first fires die in wet ditches. Wulfred's outriders leave bodies among the hayricks, and Ashwick's scouts fall back with breath enough to warn the palisade.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("seven_ash_outer_fields_to_palisade", [], "Fall back to the palisade.", [
        (call_script, "script_sod_seven_ash_resolve_outer_fields", sod_seven_ash_siege_result_held),
        (jump_to_menu, "mnu_seven_ash_palisade_staging"),
      ]),
    ]
  ),

(
    "seven_ash_outer_fields_bloodied", mnf_disable_all_keys,
    "The fields are held, but not cleanly. The smoke turns men into guesses. Some families reach the ditch late, and every captain hears the cost in the wounded carried past them.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("seven_ash_outer_fields_to_palisade_bloodied", [], "Drag the wounded through and bar the lanes.", [
        (call_script, "script_sod_seven_ash_resolve_outer_fields", sod_seven_ash_siege_result_bloodied),
        (jump_to_menu, "mnu_seven_ash_palisade_staging"),
      ]),
    ]
  ),

(
    "seven_ash_palisade_staging", mnf_disable_all_keys,
    "The ditch and palisade take the next weight. Oswin's stakes wait in the mud, Tomas counts the militia by voice, and Wulfred's larger host begins to arrive by measured waves instead of one honest rush. The next count is {reg0} attackers in {reg1} pushes.",
    "none",
    [
      (set_background_mesh, "mesh_pic_siege_sighted"),
      (call_script, "script_sod_seven_ash_prepare_palisade"),
    ],
    [
      ("seven_ash_palisade_fight", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_siege_phase_active, sod_seven_ash_siege_phase_palisade),
      ], "Stand the ditch and palisade.", [
        (modify_visitors_at_site, "scn_random_scene"),
        (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (set_visitor, 1, "trp_seven_ash_oswin_ditchwright"),
        (set_visitor, 2, "trp_seven_ash_tomas_reed"),
        (set_visitor, 3, "trp_watchman"),
        (set_visitor, 4, "trp_caravan_guard"),
        (set_visitor, 10, "trp_brigand"),
        (set_visitor, 11, "trp_henchman"),
        (set_visitor, 12, "trp_bandit"),
        (set_visitor, 13, "trp_seven_ash_halvorn_pike"),
        (set_visitor, 14, "trp_brigand"),
        (set_visitor, 15, "trp_looter"),
        (set_jump_mission, "mt_seven_ash_palisade"),
        (jump_to_scene, "scn_random_scene"),
        (change_screen_mission),
      ]),
      ("seven_ash_palisade_yield", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_siege_phase_active, sod_seven_ash_siege_phase_palisade),
      ], "Abandon the ditch and collapse toward the gate.", [
        (call_script, "script_sod_seven_ash_resolve_palisade", sod_seven_ash_siege_result_lost),
        (jump_to_menu, "mnu_seven_ash_breach_staging"),
      ]),
    ]
  ),

(
    "seven_ash_palisade_held", mnf_disable_all_keys,
    "The ditch drinks the charge. Ladders fall crooked, shieldmen stumble onto stakes, and the palisade holds long enough for the gate reserve to hear Halvorn's horns turn desperate.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("seven_ash_palisade_to_breach", [], "Send the reserve to the gate.", [
        (call_script, "script_sod_seven_ash_resolve_palisade", sod_seven_ash_siege_result_held),
        (jump_to_menu, "mnu_seven_ash_breach_staging"),
      ]),
    ]
  ),

(
    "seven_ash_palisade_bloodied", mnf_disable_all_keys,
    "The palisade holds by splinters and curses. Oswin's stakes buy time, Tomas's calls keep the line from running, but too many attackers reach the wall before they break.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("seven_ash_palisade_to_breach_bloodied", [], "Fall back before the gate is rushed.", [
        (call_script, "script_sod_seven_ash_resolve_palisade", sod_seven_ash_siege_result_bloodied),
        (jump_to_menu, "mnu_seven_ash_breach_staging"),
      ]),
    ]
  ),

(
    "seven_ash_breach_staging", mnf_disable_all_keys,
    "Halvorn Pike gathers the hard core near the gate. The breach phase will decide whether the palisade's wounds become a trap or an open throat. The gate count is {reg0} hard attackers in {reg1} brutal pushes.",
    "none",
    [
      (set_background_mesh, "mesh_pic_siege_sighted"),
      (call_script, "script_sod_seven_ash_prepare_breach"),
    ],
    [
      ("seven_ash_breach_fight", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_siege_phase_active, sod_seven_ash_siege_phase_breach),
      ], "Meet Halvorn at the breach.", [
        (modify_visitors_at_site, "scn_random_scene"),
        (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (set_visitor, 1, "trp_seven_ash_sir_aldrik_vane"),
        (set_visitor, 2, "trp_seven_ash_beren_hardhand"),
        (set_visitor, 3, "trp_watchman"),
        (set_visitor, 4, "trp_caravan_guard"),
        (set_visitor, 10, "trp_seven_ash_halvorn_pike"),
        (set_visitor, 11, "trp_brigand"),
        (set_visitor, 12, "trp_henchman"),
        (set_visitor, 13, "trp_bandit"),
        (set_visitor, 14, "trp_brigand"),
        (set_visitor, 15, "trp_henchman"),
        (set_jump_mission, "mt_seven_ash_breach"),
        (jump_to_scene, "scn_random_scene"),
        (change_screen_mission),
      ]),
      ("seven_ash_breach_yield", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_siege_phase_active, sod_seven_ash_siege_phase_breach),
      ], "Give the gate and fight through the streets.", [
        (call_script, "script_sod_seven_ash_resolve_breach", sod_seven_ash_siege_result_lost),
        (jump_to_menu, "mnu_seven_ash_inner_streets_staging"),
      ]),
    ]
  ),

(
    "seven_ash_breach_held", mnf_disable_all_keys,
    "Halvorn's push breaks against the gate reserve. Aldrik keeps the oath in public view, Beren makes the breach too costly to love, and the hard core staggers back from the throat of Ashwick.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("seven_ash_breach_to_streets", [], "Sweep the streets for fires and stragglers.", [
        (call_script, "script_sod_seven_ash_resolve_breach", sod_seven_ash_siege_result_held),
        (jump_to_menu, "mnu_seven_ash_inner_streets_staging"),
      ]),
    ]
  ),

(
    "seven_ash_breach_bloodied", mnf_disable_all_keys,
    "The gate holds, but only after the breach becomes a butcher's ledger. Halvorn is forced back, yet wounded men and frightened families are already moving toward the inner streets.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("seven_ash_breach_to_streets_bloodied", [], "Pull the line inward before fires spread.", [
        (call_script, "script_sod_seven_ash_resolve_breach", sod_seven_ash_siege_result_bloodied),
        (jump_to_menu, "mnu_seven_ash_inner_streets_staging"),
      ]),
    ]
  ),

(
    "seven_ash_inner_streets_staging", mnf_disable_all_keys,
    "The fight reaches Ashwick's doors. Mirelle's chalk marks point through alleys and cellars, while Elianor's people drag the wounded away from sparks. The street count is {reg0} attackers in {reg1} pushes.",
    "none",
    [
      (set_background_mesh, "mesh_pic_siege_sighted"),
      (call_script, "script_sod_seven_ash_prepare_inner_streets"),
    ],
    [
      ("seven_ash_inner_streets_fight", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_siege_phase_active, sod_seven_ash_siege_phase_inner_streets),
      ], "Fight through the doors, fires, and cellars.", [
        (modify_visitors_at_site, "scn_random_scene"),
        (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (set_visitor, 1, "trp_seven_ash_mirelle_voss"),
        (set_visitor, 2, "trp_seven_ash_sister_elianor"),
        (set_visitor, 3, "trp_farmer"),
        (set_visitor, 4, "trp_watchman"),
        (set_visitor, 10, "trp_brigand"),
        (set_visitor, 11, "trp_bandit"),
        (set_visitor, 12, "trp_henchman"),
        (set_visitor, 13, "trp_looter"),
        (set_visitor, 14, "trp_brigand"),
        (set_visitor, 15, "trp_seven_ash_maud_ledger"),
        (set_jump_mission, "mt_seven_ash_inner_streets"),
        (jump_to_scene, "scn_random_scene"),
        (change_screen_mission),
      ]),
      ("seven_ash_inner_streets_yield", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_siege_phase_active, sod_seven_ash_siege_phase_inner_streets),
      ], "Abandon the streets and run for the churchyard.", [
        (call_script, "script_sod_seven_ash_resolve_inner_streets", sod_seven_ash_siege_result_lost),
        (jump_to_menu, "mnu_seven_ash_churchyard_staging"),
      ]),
    ]
  ),

(
    "seven_ash_inner_streets_held", mnf_disable_all_keys,
    "The fires are smothered before they join hands. Mirelle's exits stay secret, Elianor's wounded reach shelter, and Ashwick falls back by lanes it chose instead of lanes it lost.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("seven_ash_inner_streets_to_churchyard", [], "Gather at the churchyard wall.", [
        (call_script, "script_sod_seven_ash_resolve_inner_streets", sod_seven_ash_siege_result_held),
        (jump_to_menu, "mnu_seven_ash_churchyard_staging"),
      ]),
    ]
  ),

(
    "seven_ash_inner_streets_bloodied", mnf_disable_all_keys,
    "The streets hold only because people pay for every doorway. Some fires are beaten down. Some are left to burn. The last line forms around the churchyard with smoke in its mouth.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("seven_ash_inner_streets_to_churchyard_bloodied", [], "Carry who can be carried to the churchyard.", [
        (call_script, "script_sod_seven_ash_resolve_inner_streets", sod_seven_ash_siege_result_bloodied),
        (jump_to_menu, "mnu_seven_ash_churchyard_staging"),
      ]),
    ]
  ),

(
    "seven_ash_churchyard_staging", mnf_disable_all_keys,
    "The churchyard wall is the final line. Wulfred comes close enough for his name to matter, and the last count is {reg0} attackers in {reg1} pushes. Ashwick's cost will be counted after this wall either holds or breaks.",
    "none",
    [
      (set_background_mesh, "mesh_pic_siege_sighted"),
      (call_script, "script_sod_seven_ash_prepare_churchyard"),
    ],
    [
      ("seven_ash_churchyard_fight", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_siege_phase_active, sod_seven_ash_siege_phase_churchyard),
      ], "Make the churchyard stand.", [
        (modify_visitors_at_site, "scn_random_scene"),
        (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (set_visitor, 1, "trp_seven_ash_mother_hilda"),
        (set_visitor, 2, "trp_seven_ash_garric_ashbow"),
        (set_visitor, 3, "trp_seven_ash_oswin_ditchwright"),
        (set_visitor, 4, "trp_seven_ash_sir_aldrik_vane"),
        (set_visitor, 5, "trp_seven_ash_mirelle_voss"),
        (set_visitor, 6, "trp_seven_ash_tomas_reed"),
        (set_visitor, 7, "trp_seven_ash_beren_hardhand"),
        (set_visitor, 8, "trp_seven_ash_sister_elianor"),
        (set_visitor, 10, "trp_seven_ash_wulfred_carr"),
        (set_visitor, 11, "trp_seven_ash_halvorn_pike"),
        (set_visitor, 12, "trp_brigand"),
        (set_visitor, 13, "trp_henchman"),
        (set_visitor, 14, "trp_bandit"),
        (set_visitor, 15, "trp_brigand"),
        (set_jump_mission, "mt_seven_ash_churchyard"),
        (jump_to_scene, "scn_random_scene"),
        (change_screen_mission),
      ]),
      ("seven_ash_churchyard_surrender", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_siege_phase_active, sod_seven_ash_siege_phase_churchyard),
      ], "Break the last line and let Wulfred take Ashwick.", [
        (call_script, "script_sod_seven_ash_resolve_churchyard", sod_seven_ash_siege_result_lost, sod_seven_ash_wulfred_wins),
        (jump_to_menu, "mnu_seven_ash_aftermath_staging"),
      ]),
    ]
  ),

(
    "seven_ash_churchyard_wulfred_captured", mnf_disable_all_keys,
    "Wulfred Carr is dragged down alive below the churchyard wall. The village does not cheer at first. It listens for another horn, then hears none.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("seven_ash_churchyard_capture_to_aftermath", [], "Bind Wulfred and count the cost.", [
        (call_script, "script_sod_seven_ash_resolve_churchyard", sod_seven_ash_siege_result_held, sod_seven_ash_wulfred_captured),
        (jump_to_menu, "mnu_seven_ash_aftermath_staging"),
      ]),
    ]
  ),

(
    "seven_ash_churchyard_wulfred_killed", mnf_disable_all_keys,
    "Wulfred Carr dies within sight of the church door. His hard men break around the fact of it, but victory arrives with blood on both hands.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("seven_ash_churchyard_kill_to_aftermath", [], "Let the bells sound and count the cost.", [
        (call_script, "script_sod_seven_ash_resolve_churchyard", sod_seven_ash_siege_result_bloodied, sod_seven_ash_wulfred_killed),
        (jump_to_menu, "mnu_seven_ash_aftermath_staging"),
      ]),
    ]
  ),

(
    "seven_ash_churchyard_wulfred_escaped", mnf_disable_all_keys,
    "The churchyard holds, but Wulfred is carried or dragged out through smoke before anyone can swear whose blade found him. Ashwick survives with a road still watching it.",
    "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("seven_ash_churchyard_escape_to_aftermath", [], "Secure the wall and count the cost.", [
        (call_script, "script_sod_seven_ash_resolve_churchyard", sod_seven_ash_siege_result_bloodied, sod_seven_ash_wulfred_escaped),
        (jump_to_menu, "mnu_seven_ash_aftermath_staging"),
      ]),
    ]
  ),

(
    "seven_ash_aftermath_staging", mnf_disable_all_keys,
    "The siege is over. Reeve Martin counts {reg0} civilian dead and {reg1} burned homes. Mother Hilda names {reg2} of the seven defenders still able to answer. Wulfred's fate, prisoner treatment, promises kept, and Ashwick's future are now matters for witnesses instead of horns.",
    "none",
    [
      (set_background_mesh, "mesh_pic_siege_sighted"),
      (call_script, "script_sod_seven_ash_apply_immediate_aftermath"),
    ],
    [
      ("seven_ash_aftermath_record", [], "Record the first count of the aftermath.", [
        (setup_quest_text, "qst_seven_ash_aftermath"),
        (str_store_string, s2, "@The first aftermath count records civilian deaths, burned homes, surviving defenders, Wulfred's state, prisoner treatment, promises kept, and Ashwick's settlement outcome. Defender epilogues and companion offers remain to be resolved through dialogue."),
        (add_quest_note_from_sreg, "qst_seven_ash_aftermath", 1, s2, 0),
        (jump_to_menu, "mnu_seven_ash_aftermath_defenders"),
      ]),
    ]
  ),

(
    "seven_ash_aftermath_defenders", mnf_disable_all_keys,
    "Ashwick's survivors wait in small knots instead of one crowd. Each defender deserves a separate word: not a reward screen, but a reckoning with what they saw you do.",
    "none",
    [
      (set_background_mesh, "mesh_pic_siege_sighted"),
    ],
    [
      ("seven_ash_aftermath_garric", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_aftermath),
        (quest_get_slot, ":survivors", "qst_seven_ash_ultimatum", slot_quest_seven_ash_survival_bitmask),
        (store_and, ":alive", ":survivors", sod_seven_ash_defender_garric),
        (gt, ":alive", 0),
        (quest_get_slot, ":joined", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_joined_bitmask),
        (store_and, ":joined_bit", ":joined", sod_seven_ash_defender_garric),
        (eq, ":joined_bit", 0),
        (quest_get_slot, ":stayed", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_stayed_bitmask),
        (store_and, ":stayed_bit", ":stayed", sod_seven_ash_defender_garric),
        (eq, ":stayed_bit", 0),
        (quest_get_slot, ":refused", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_refusal_bitmask),
        (store_and, ":refused_bit", ":refused", sod_seven_ash_defender_garric),
        (eq, ":refused_bit", 0),
      ], "Speak with Garric at the watch platform.", [
        (start_map_conversation, "trp_seven_ash_garric_ashbow"),
      ]),
      ("seven_ash_aftermath_oswin", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_aftermath),
        (quest_get_slot, ":survivors", "qst_seven_ash_ultimatum", slot_quest_seven_ash_survival_bitmask),
        (store_and, ":alive", ":survivors", sod_seven_ash_defender_oswin),
        (gt, ":alive", 0),
        (quest_get_slot, ":joined", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_joined_bitmask),
        (store_and, ":joined_bit", ":joined", sod_seven_ash_defender_oswin),
        (eq, ":joined_bit", 0),
        (quest_get_slot, ":stayed", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_stayed_bitmask),
        (store_and, ":stayed_bit", ":stayed", sod_seven_ash_defender_oswin),
        (eq, ":stayed_bit", 0),
        (quest_get_slot, ":refused", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_refusal_bitmask),
        (store_and, ":refused_bit", ":refused", sod_seven_ash_defender_oswin),
        (eq, ":refused_bit", 0),
      ], "Speak with Oswin by the repaired gate.", [
        (start_map_conversation, "trp_seven_ash_oswin_ditchwright"),
      ]),
      ("seven_ash_aftermath_aldrik", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_aftermath),
        (quest_get_slot, ":survivors", "qst_seven_ash_ultimatum", slot_quest_seven_ash_survival_bitmask),
        (store_and, ":alive", ":survivors", sod_seven_ash_defender_aldrik),
        (gt, ":alive", 0),
        (quest_get_slot, ":joined", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_joined_bitmask),
        (store_and, ":joined_bit", ":joined", sod_seven_ash_defender_aldrik),
        (eq, ":joined_bit", 0),
        (quest_get_slot, ":stayed", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_stayed_bitmask),
        (store_and, ":stayed_bit", ":stayed", sod_seven_ash_defender_aldrik),
        (eq, ":stayed_bit", 0),
        (quest_get_slot, ":refused", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_refusal_bitmask),
        (store_and, ":refused_bit", ":refused", sod_seven_ash_defender_aldrik),
        (eq, ":refused_bit", 0),
      ], "Speak with Aldrik beside the shield on the gate.", [
        (start_map_conversation, "trp_seven_ash_sir_aldrik_vane"),
      ]),
      ("seven_ash_aftermath_mirelle", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_aftermath),
        (quest_get_slot, ":survivors", "qst_seven_ash_ultimatum", slot_quest_seven_ash_survival_bitmask),
        (store_and, ":alive", ":survivors", sod_seven_ash_defender_mirelle),
        (gt, ":alive", 0),
        (quest_get_slot, ":joined", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_joined_bitmask),
        (store_and, ":joined_bit", ":joined", sod_seven_ash_defender_mirelle),
        (eq, ":joined_bit", 0),
        (quest_get_slot, ":stayed", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_stayed_bitmask),
        (store_and, ":stayed_bit", ":stayed", sod_seven_ash_defender_mirelle),
        (eq, ":stayed_bit", 0),
        (quest_get_slot, ":refused", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_refusal_bitmask),
        (store_and, ":refused_bit", ":refused", sod_seven_ash_defender_mirelle),
        (eq, ":refused_bit", 0),
      ], "Speak with Mirelle by the chalk-marked alleys.", [
        (start_map_conversation, "trp_seven_ash_mirelle_voss"),
      ]),
      ("seven_ash_aftermath_tomas", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_aftermath),
        (quest_get_slot, ":survivors", "qst_seven_ash_ultimatum", slot_quest_seven_ash_survival_bitmask),
        (store_and, ":alive", ":survivors", sod_seven_ash_defender_tomas),
        (gt, ":alive", 0),
        (quest_get_slot, ":joined", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_joined_bitmask),
        (store_and, ":joined_bit", ":joined", sod_seven_ash_defender_tomas),
        (eq, ":joined_bit", 0),
        (quest_get_slot, ":stayed", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_stayed_bitmask),
        (store_and, ":stayed_bit", ":stayed", sod_seven_ash_defender_tomas),
        (eq, ":stayed_bit", 0),
        (quest_get_slot, ":refused", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_refusal_bitmask),
        (store_and, ":refused_bit", ":refused", sod_seven_ash_defender_tomas),
        (eq, ":refused_bit", 0),
      ], "Speak with Tomas near the militia rows.", [
        (start_map_conversation, "trp_seven_ash_tomas_reed"),
      ]),
      ("seven_ash_aftermath_beren", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_aftermath),
        (quest_get_slot, ":survivors", "qst_seven_ash_ultimatum", slot_quest_seven_ash_survival_bitmask),
        (store_and, ":alive", ":survivors", sod_seven_ash_defender_beren),
        (gt, ":alive", 0),
        (quest_get_slot, ":joined", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_joined_bitmask),
        (store_and, ":joined_bit", ":joined", sod_seven_ash_defender_beren),
        (eq, ":joined_bit", 0),
        (quest_get_slot, ":stayed", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_stayed_bitmask),
        (store_and, ":stayed_bit", ":stayed", sod_seven_ash_defender_beren),
        (eq, ":stayed_bit", 0),
        (quest_get_slot, ":refused", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_refusal_bitmask),
        (store_and, ":refused_bit", ":refused", sod_seven_ash_defender_beren),
        (eq, ":refused_bit", 0),
      ], "Speak with Beren where the gate beam cracked.", [
        (start_map_conversation, "trp_seven_ash_beren_hardhand"),
      ]),
      ("seven_ash_aftermath_elianor", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_aftermath),
        (quest_get_slot, ":survivors", "qst_seven_ash_ultimatum", slot_quest_seven_ash_survival_bitmask),
        (store_and, ":alive", ":survivors", sod_seven_ash_defender_elianor),
        (gt, ":alive", 0),
        (quest_get_slot, ":joined", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_joined_bitmask),
        (store_and, ":joined_bit", ":joined", sod_seven_ash_defender_elianor),
        (eq, ":joined_bit", 0),
        (quest_get_slot, ":stayed", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_stayed_bitmask),
        (store_and, ":stayed_bit", ":stayed", sod_seven_ash_defender_elianor),
        (eq, ":stayed_bit", 0),
        (quest_get_slot, ":refused", "qst_seven_ash_ultimatum", slot_quest_seven_ash_companion_refusal_bitmask),
        (store_and, ":refused_bit", ":refused", sod_seven_ash_defender_elianor),
        (eq, ":refused_bit", 0),
      ], "Speak with Elianor in the church infirmary.", [
        (start_map_conversation, "trp_seven_ash_sister_elianor"),
      ]),
      ("seven_ash_aftermath_done_for_now", [], "Leave the aftermath for now.", [
        (jump_to_menu, "mnu_start_phase_2"),
      ]),
    ]
  ),
]

