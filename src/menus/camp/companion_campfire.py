MENUS = [
("companion_campfire", mnf_scale_picture|mnf_enable_hot_keys,
   "{s1}",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (call_script, "script_sod_companion_describe_campfire_to_s1"),
    ],
    [
      ("companion_campfire_borcha_scout", [
          (main_party_has_troop, "trp_npc1"),
        ], "Ask Borcha to serve as Scout.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc1", sod_companion_role_scout),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_borcha_quartermaster", [
          (main_party_has_troop, "trp_npc1"),
        ], "Ask Borcha to watch the road stores.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc1", sod_companion_role_quartermaster),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_marnid_quartermaster", [
          (main_party_has_troop, "trp_npc2"),
        ], "Ask Marnid to serve as Quartermaster.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc2", sod_companion_role_quartermaster),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_marnid_envoy", [
          (main_party_has_troop, "trp_npc2"),
        ], "Ask Marnid to serve as Envoy.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc2", sod_companion_role_envoy),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_ymira_surgeon", [
          (main_party_has_troop, "trp_npc3"),
        ], "Ask Ymira to serve as Surgeon.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc3", sod_companion_role_surgeon),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_ymira_envoy", [
          (main_party_has_troop, "trp_npc3"),
        ], "Ask Ymira to serve as Envoy.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc3", sod_companion_role_envoy),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_rolf_envoy", [
          (main_party_has_troop, "trp_npc4"),
        ], "Ask Rolf to serve as Envoy.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc4", sod_companion_role_envoy),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_rolf_captain", [
          (main_party_has_troop, "trp_npc4"),
        ], "Ask Rolf to serve as Captain.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc4", sod_companion_role_captain),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_baheshtur_scout", [
          (main_party_has_troop, "trp_npc5"),
        ], "Ask Baheshtur to serve as Scout.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc5", sod_companion_role_scout),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_baheshtur_captain", [
          (main_party_has_troop, "trp_npc5"),
        ], "Ask Baheshtur to command the riders.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc5", sod_companion_role_captain),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_firentis_captain", [
          (main_party_has_troop, "trp_npc6"),
        ], "Ask Firentis to serve as Captain.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc6", sod_companion_role_captain),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_firentis_envoy", [
          (main_party_has_troop, "trp_npc6"),
        ], "Ask Firentis to serve as Envoy.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc6", sod_companion_role_envoy),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_deshavi_scout", [
          (main_party_has_troop, "trp_npc7"),
        ], "Ask Deshavi to serve as Scout.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc7", sod_companion_role_scout),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_deshavi_spymaster", [
          (main_party_has_troop, "trp_npc7"),
        ], "Ask Deshavi to serve as Spymaster.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc7", sod_companion_role_spymaster),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_matheld_captain", [
          (main_party_has_troop, "trp_npc8"),
        ], "Ask Matheld to serve as Captain.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc8", sod_companion_role_captain),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_alayen_envoy", [
          (main_party_has_troop, "trp_npc9"),
        ], "Ask Alayen to serve as Envoy.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc9", sod_companion_role_envoy),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_alayen_captain", [
          (main_party_has_troop, "trp_npc9"),
        ], "Ask Alayen to serve as Captain.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc9", sod_companion_role_captain),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_nizar_captain", [
          (main_party_has_troop, "trp_npc13"),
        ], "Ask Nizar to serve as Captain.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc13", sod_companion_role_captain),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_nizar_scout", [
          (main_party_has_troop, "trp_npc13"),
        ], "Ask Nizar to scout for bold openings.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc13", sod_companion_role_scout),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_bunduk_captain", [
          (main_party_has_troop, "trp_npc10"),
        ], "Ask Bunduk to serve as Captain.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc10", sod_companion_role_captain),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_bunduk_quartermaster", [
          (main_party_has_troop, "trp_npc10"),
        ], "Ask Bunduk to watch the common soldiers' stores.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc10", sod_companion_role_quartermaster),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_katrin_quartermaster", [
          (main_party_has_troop, "trp_npc11"),
        ], "Ask Katrin to serve as Quartermaster.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc11", sod_companion_role_quartermaster),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_katrin_surgeon", [
          (main_party_has_troop, "trp_npc11"),
        ], "Ask Katrin to tend the camp as Surgeon.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc11", sod_companion_role_surgeon),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_jeremus_surgeon", [
          (main_party_has_troop, "trp_npc12"),
        ], "Ask Jeremus to serve as Surgeon.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc12", sod_companion_role_surgeon),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_jeremus_envoy", [
          (main_party_has_troop, "trp_npc12"),
        ], "Ask Jeremus to serve as Envoy.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc12", sod_companion_role_envoy),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_klethi_spymaster", [
          (main_party_has_troop, "trp_npc16"),
        ], "Ask Klethi to serve as Spymaster.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc16", sod_companion_role_spymaster),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_klethi_scout", [
          (main_party_has_troop, "trp_npc16"),
        ], "Ask Klethi to serve as Scout.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc16", sod_companion_role_scout),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_lezalit_captain", [
          (main_party_has_troop, "trp_npc14"),
        ], "Ask Lezalit to serve as Captain.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc14", sod_companion_role_captain),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_lezalit_engineer", [
          (main_party_has_troop, "trp_npc14"),
        ], "Ask Lezalit to serve as Engineer.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc14", sod_companion_role_engineer),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_artimenner_engineer", [
          (main_party_has_troop, "trp_npc15"),
        ], "Ask Artimenner to serve as Engineer.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc15", sod_companion_role_engineer),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_artimenner_quartermaster", [
          (main_party_has_troop, "trp_npc15"),
        ], "Ask Artimenner to organize tools and stores.",
        [
          (call_script, "script_sod_companion_assign_role", "trp_npc15", sod_companion_role_quartermaster),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_borcha_road_keeps_own_start", [
          (main_party_has_troop, "trp_npc1"),
          (troop_slot_eq, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc1", slot_troop_companion_approval, 45),
        ], "Speak with Borcha about The Road Keeps Its Own.",
        [
          (troop_set_slot, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Borcha crouches near the fire and draws a crooked line in the dirt. 'Too clean a road means somebody swept it. Raiders, maybe. Men waiting to be called ghosts.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_borcha_road_keeps_own_trust", [
          (main_party_has_troop, "trp_npc1"),
          (troop_slot_eq, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Trust Borcha and set scouts on the hidden route.",
        [
          (call_script, "script_sod_companion_start_borcha_road_incident", 1),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_safe_roadcraft, 3),
          (display_message, "@Borcha nods once. 'Good. We ask who saw the road first. Bleed later, if bleeding has to happen.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_borcha_road_keeps_own_profit", [
          (main_party_has_troop, "trp_npc1"),
          (troop_slot_eq, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Use Borcha's route to bait raiders for plunder.",
        [
          (call_script, "script_sod_companion_start_borcha_road_incident", 2),
          (call_script, "script_sod_companion_shift_approval", "trp_npc1", 1),
          (display_message, "@Borcha snorts. 'Dirty, but not stupid. Ask at the road town. Bait has a short life if the hook is slow.'", 0xCCCC66),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_borcha_road_keeps_own_dismiss", [
          (main_party_has_troop, "trp_npc1"),
          (troop_slot_eq, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Tell Borcha the road can wait.",
        [
          (call_script, "script_sod_companion_shift_approval", "trp_npc1", -4),
          (display_message, "@Borcha smooths the dirt with his boot. 'Roads wait. Knives do not.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_borcha_road_keeps_own_resolve", [
          (main_party_has_troop, "trp_npc1"),
          (eq, "$g_sod_borcha_road_pending", 1),
          (eq, "$g_sod_borcha_road_witnessed", 1),
          (eq, "$g_sod_borcha_road_confronted", 1),
          (troop_slot_eq, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Follow Borcha's road plan to its end.",
        [
          (jump_to_menu, "mnu_borcha_road_keeps_own"),
        ]
      ),
      ("companion_campfire_borcha_road_keeps_own_hard", [
          (main_party_has_troop, "trp_npc1"),
          (eq, "$g_sod_borcha_road_pending", 1),
          (eq, "$g_sod_borcha_road_witnessed", 1),
          (eq, "$g_sod_borcha_road_confronted", 1),
          (troop_slot_eq, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Press the route hard for profit.",
        [
          (jump_to_menu, "mnu_borcha_road_keeps_own"),
        ]
      ),
      ("companion_campfire_marnid_honest_price_start", [
          (main_party_has_troop, "trp_npc2"),
          (troop_slot_eq, "trp_npc2", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc2", slot_troop_companion_approval, 45),
        ], "Speak with Marnid about The Honest Price.",
        [
          (troop_set_slot, "trp_npc2", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Marnid opens a careful ledger. 'There are clean profits, necessary profits, and profits that poison the next road. I would rather know which column we are using.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_marnid_honest_price_clean", [
          (main_party_has_troop, "trp_npc2"),
          (troop_slot_eq, "trp_npc2", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Back Marnid's clean trade contacts.",
        [
          (call_script, "script_sod_companion_start_marnid_market_incident", 1),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_orderly_profit, 3),
          (display_message, "@Marnid marks three names and crosses out two. 'Good. Now we ask the market which names are missing.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_marnid_honest_price_dirty", [
          (main_party_has_troop, "trp_npc2"),
          (troop_slot_eq, "trp_npc2", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Use Marnid's contacts for dirtier prisoner profit.",
        [
          (call_script, "script_sod_companion_start_marnid_market_incident", 2),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_dirty_profit, 2),
          (display_message, "@Marnid closes the ledger slowly. 'Profitable, yes. But some accounts charge interest in sleep. We ask the market before it collects.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_marnid_honest_price_resolve", [
          (main_party_has_troop, "trp_npc2"),
          (eq, "$g_sod_marnid_market_pending", 1),
          (ge, "$g_sod_marnid_market_evidence", 1),
          (eq, "$g_sod_marnid_market_confronted", 1),
          (troop_slot_eq, "trp_npc2", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Settle The Honest Price cleanly.",
        [
          (jump_to_menu, "mnu_marnid_honest_price"),
        ]
      ),
      ("companion_campfire_marnid_honest_price_hard", [
          (main_party_has_troop, "trp_npc2"),
          (eq, "$g_sod_marnid_market_pending", 1),
          (ge, "$g_sod_marnid_market_evidence", 1),
          (eq, "$g_sod_marnid_market_confronted", 1),
          (troop_slot_eq, "trp_npc2", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Squeeze The Honest Price for every denar.",
        [
          (jump_to_menu, "mnu_marnid_honest_price"),
        ]
      ),
      ("companion_campfire_ymira_mercy_start", [
          (main_party_has_troop, "trp_npc3"),
          (troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc3", slot_troop_companion_approval, 45),
        ], "Speak with Ymira about Mercy Under Arms.",
        [
          (troop_set_slot, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Ymira watches the prisoners beyond the fire. 'A victory does not end when the shouting stops. That is when command shows its real face.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_ymira_mercy_spare", [
          (main_party_has_troop, "trp_npc3"),
          (troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Promise Ymira the helpless will be protected.",
        [
          (troop_set_slot, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_free_captives, 3),
          (display_message, "@Ymira lets out a breath she had been holding. 'Then mercy has a place in this company, not just a corner where it hides.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_ymira_mercy_ransom", [
          (main_party_has_troop, "trp_npc3"),
          (troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Tell Ymira mercy must answer to ransom and supply.",
        [
          (troop_set_slot, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc3", -2),
          (display_message, "@Ymira nods, but not happily. 'I know supplies matter. I only fear the day every person becomes a line in the stores.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_ymira_mercy_dismiss", [
          (main_party_has_troop, "trp_npc3"),
          (troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Tell Ymira not every wound can be your concern.",
        [
          (call_script, "script_sod_companion_shift_approval", "trp_npc3", -5),
          (display_message, "@Ymira looks back to the dark beyond camp. 'No. Only the ones we choose not to see.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_ymira_mercy_resolve", [
          (main_party_has_troop, "trp_npc3"),
          (troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve Mercy Under Arms with protection.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc3", 1),
          (display_message, "@The captives are guarded, fed, and sent toward safety. Ymira does not call it victory. She calls it proof.", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_ymira_mercy_hard", [
          (main_party_has_troop, "trp_npc3"),
          (troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve Mercy Under Arms with hard necessity.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc3", 0),
          (display_message, "@The army is supplied and the captives are accounted for, but Ymira's thanks do not come easily. 'Necessary should never become easy.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_rolf_name_start", [
          (main_party_has_troop, "trp_npc4"),
          (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc4", slot_troop_companion_approval, 45),
        ], "Speak with Rolf about A Name Worth Wearing.",
        [
          (troop_set_slot, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Rolf adjusts his cloak as if a hall of nobles were watching. 'There are men who inherit names, and lesser men who question them.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_rolf_name_earn", [
          (main_party_has_troop, "trp_npc4"),
          (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Tell Rolf a name is proven by conduct.",
        [
          (troop_set_slot, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_hard_victory, 2),
          (display_message, "@Rolf begins to object, then smiles. 'Naturally. A great name improves the deeds beneath it.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_rolf_name_defend", [
          (main_party_has_troop, "trp_npc4"),
          (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Publicly defend Rolf's dignity.",
        [
          (troop_set_slot, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc4", 3),
          (display_message, "@Rolf's bow is magnificent. 'At last, someone here understands lineage as a civic necessity.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_rolf_name_expose", [
          (main_party_has_troop, "trp_npc4"),
          (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Force Rolf to drop the performance.",
        [
          (troop_set_slot, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc4", -5),
          (display_message, "@Rolf's smile stays in place a moment too long. 'How brave, to strip a cloak and call the shivering man honest.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_rolf_name_resolve", [
          (main_party_has_troop, "trp_npc4"),
          (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve A Name Worth Wearing by letting Rolf earn it.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc4", 1),
          (display_message, "@Rolf stands before the company without embellishing the tale. Somehow, the name sounds larger for carrying less smoke.", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_rolf_name_hard", [
          (main_party_has_troop, "trp_npc4"),
          (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve A Name Worth Wearing by preserving the grand claim.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc4", 0),
          (display_message, "@The story survives intact. Rolf is grateful, proud, and a little more trapped inside it.", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_baheshtur_saddle_start", [
          (main_party_has_troop, "trp_npc5"),
          (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc5", slot_troop_companion_approval, 45),
        ], "Speak with Baheshtur about The Unbroken Saddle.",
        [
          (troop_set_slot, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Baheshtur tightens a saddle strap beside the fire. 'A saddle can carry a man or mark him owned. The difference is who chose the road.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_baheshtur_saddle_ride", [
          (main_party_has_troop, "trp_npc5"),
          (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Ride hard against the steppe rival before he gathers strength.",
        [
          (troop_set_slot, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_hard_victory, 2),
          (display_message, "@Baheshtur's nod is small and fierce. 'Good. Let him learn that open ground does not belong only to raiders.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_baheshtur_saddle_free", [
          (main_party_has_troop, "trp_npc5"),
          (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Offer captured riders honorable freedom if they swear freely.",
        [
          (troop_set_slot, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc5", 4),
          (display_message, "@Baheshtur watches you carefully. 'An oath taken by a free man has weight. Anything else is rope.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_baheshtur_saddle_bargain", [
          (main_party_has_troop, "trp_npc5"),
          (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Buy peace with tribute and let the insult pass.",
        [
          (troop_set_slot, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_black_khergit_tribute, 1),
          (display_message, "@Baheshtur looks toward the horse lines. 'A paid wolf is still a wolf. He only learns your purse has meat in it.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_baheshtur_saddle_resolve", [
          (main_party_has_troop, "trp_npc5"),
          (eq, "$g_sod_baheshtur_saddle_witnessed", 1),
          (eq, "$g_sod_baheshtur_saddle_confronted", 1),
          (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve The Unbroken Saddle through chosen loyalty.",
        [
          (assign, "$g_sod_baheshtur_saddle_result_grade", 3),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc5", 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc5"),
          (display_message, "@The rival's riders scatter, and those who remain do so by their own word. Baheshtur says only, 'Now they ride with us, not under us.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_baheshtur_saddle_hard", [
          (main_party_has_troop, "trp_npc5"),
          (eq, "$g_sod_baheshtur_saddle_witnessed", 1),
          (eq, "$g_sod_baheshtur_saddle_confronted", 1),
          (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve The Unbroken Saddle by forcing submission.",
        [
          (assign, "$g_sod_baheshtur_saddle_result_grade", 1),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc5", 0),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc5"),
          (display_message, "@The riders obey. Baheshtur does not mistake obedience for loyalty. 'You have broken the saddle in. Perhaps too well.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_firentis_debt_start", [
          (main_party_has_troop, "trp_npc6"),
          (troop_slot_eq, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc6", slot_troop_companion_approval, 45),
        ], "Speak with Firentis about Debt of the Sword.",
        [
          (troop_set_slot, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Firentis studies the edge of his blade. 'A sword remembers what the hand asks of it. So do the living.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_firentis_debt_restitution", [
          (main_party_has_troop, "trp_npc6"),
          (troop_slot_eq, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Back Firentis in making restitution.",
        [
          (troop_set_slot, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_help_village, 2),
          (display_message, "@Firentis bows his head. 'Restitution will not make the dead answer. It may still keep the living from joining them.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_firentis_debt_confess", [
          (main_party_has_troop, "trp_npc6"),
          (troop_slot_eq, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Have Firentis confess publicly and accept judgment.",
        [
          (troop_set_slot, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc6", 2),
          (display_message, "@Firentis looks afraid, then relieved by the fear. 'Then let truth do what steel cannot.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_firentis_debt_silence", [
          (main_party_has_troop, "trp_npc6"),
          (troop_slot_eq, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Bury Firentis's past to preserve the company.",
        [
          (troop_set_slot, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc6", -4),
          (display_message, "@Firentis sheathes the blade carefully. 'A buried thing is not absolved. It is only waiting.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_firentis_debt_resolve", [
          (main_party_has_troop, "trp_npc6"),
          (troop_slot_eq, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve Debt of the Sword through restitution.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc6", 1),
          (display_message, "@The debt is not erased, but it is named and answered. Firentis stands lighter, as if service has become more than punishment.", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_firentis_debt_hard", [
          (main_party_has_troop, "trp_npc6"),
          (troop_slot_eq, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve Debt of the Sword by silencing the matter.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc6", 0),
          (display_message, "@The matter goes quiet. Firentis stays, but his obedience has the shape of a sentence.", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_jeremus_hands_start", [
          (main_party_has_troop, "trp_npc12"),
          (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc12", slot_troop_companion_approval, 45),
        ], "Speak with Jeremus about Hands That Will Not Harden.",
        [
          (troop_set_slot, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Jeremus cleans a needle until it catches the firelight. 'There will be a day when we have too many wounded and too little time. I fear what that day will teach us.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_jeremus_hands_civilians", [
          (main_party_has_troop, "trp_npc12"),
          (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Promise Jeremus that civilians and helpless wounded come first.",
        [
          (troop_set_slot, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_free_captives, 3),
          (display_message, "@Jeremus closes his eyes for a moment. 'Then we will still be an army, but not only an army.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_jeremus_hands_triage", [
          (main_party_has_troop, "trp_npc12"),
          (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Set a hard triage order: save those who can still be saved.",
        [
          (troop_set_slot, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc12", 1),
          (display_message, "@Jeremus nods sadly. 'Cruel arithmetic, but not cruelty. I can work with that difference.'", 0xCCCC66),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_jeremus_hands_soldiers", [
          (main_party_has_troop, "trp_npc12"),
          (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Tell Jeremus the company's soldiers come before all others.",
        [
          (troop_set_slot, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc12", -4),
          (display_message, "@Jeremus folds the clean cloth with care. 'Then I pray our banner never becomes the measure of a life.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_jeremus_hands_resolve", [
          (main_party_has_troop, "trp_npc12"),
          (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve Hands That Will Not Harden with mercy under pressure.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc12", 1),
          (display_message, "@The wounded are sorted without rank deciding who deserves breath. Jeremus looks exhausted, but not defeated.", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_jeremus_hands_hard", [
          (main_party_has_troop, "trp_npc12"),
          (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve Hands That Will Not Harden by saving only company strength.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc12", 0),
          (display_message, "@The company recovers faster. Jeremus does not argue with the result. He only asks who will heal what the result did to you.", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_bunduk_line_start", [
          (main_party_has_troop, "trp_npc10"),
          (troop_slot_eq, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc10", slot_troop_companion_approval, 45),
        ], "Speak with Bunduk about The Men Who Hold the Line.",
        [
          (troop_set_slot, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Bunduk checks a crossbow string twice before speaking. 'Men in the line know when officers are spending them. They know before the officers do.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_bunduk_line_advocate", [
          (main_party_has_troop, "trp_npc10"),
          (troop_slot_eq, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Let Bunduk speak for the common soldiers.",
        [
          (troop_set_slot, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_train_troops, 2),
          (display_message, "@Bunduk nods. 'Good. They do not need soft words. They need boots, bolts, pay, and orders that are not stupid.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_bunduk_line_supplies", [
          (main_party_has_troop, "trp_npc10"),
          (troop_slot_eq, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Back Bunduk's demand for fair stores and watches.",
        [
          (troop_set_slot, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_food_security, 2),
          (display_message, "@Bunduk gives a short laugh. 'Amazing thing, feeding men before asking them to die. Should write a book.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_bunduk_line_crackdown", [
          (main_party_has_troop, "trp_npc10"),
          (troop_slot_eq, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Tell Bunduk the line needs harsher discipline, not complaints.",
        [
          (troop_set_slot, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc10", -5),
          (display_message, "@Bunduk's face hardens. 'Aye. I have heard officers say that just before blaming dead men for obeying.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_bunduk_line_resolve", [
          (main_party_has_troop, "trp_npc10"),
          (troop_slot_eq, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve The Men Who Hold the Line by backing the soldiers.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc10", 1),
          (display_message, "@The line gets better watches, fairer stores, and orders worth obeying. Bunduk only says, 'Now they might live long enough to complain properly.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_bunduk_line_hard", [
          (main_party_has_troop, "trp_npc10"),
          (troop_slot_eq, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve The Men Who Hold the Line by enforcing command authority.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc10", 0),
          (display_message, "@The line obeys. Bunduk stays with it, but his salute looks like something nailed to a door.", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_katrin_coin_start", [
          (main_party_has_troop, "trp_npc11"),
          (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc11", slot_troop_companion_approval, 45),
        ], "Speak with Katrin about The Last Coin in Camp.",
        [
          (troop_set_slot, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Katrin drops a small coin into an empty cup. 'That is the sound of a grand plan after supper, wages, and bandages have had their say.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_katrin_coin_stores", [
          (main_party_has_troop, "trp_npc11"),
          (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Put the last coin toward stores, wages, and medicine.",
        [
          (troop_set_slot, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_food_security, 3),
          (display_message, "@Katrin sniffs. 'Sensible. Dangerous habit, that. Keep it up and the camp may start expecting to live.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_katrin_coin_refugees", [
          (main_party_has_troop, "trp_npc11"),
          (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Stretch the stores to feed refugees without starving the camp.",
        [
          (troop_set_slot, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_help_village, 2),
          (display_message, "@Katrin begins counting portions under her breath. 'Mercy with arithmetic. Harder than speeches, better for everyone.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_katrin_coin_glory", [
          (main_party_has_troop, "trp_npc11"),
          (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Spend the last coin on a bold opportunity instead.",
        [
          (troop_set_slot, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc11", -5),
          (display_message, "@Katrin folds her arms. 'Of course. A hungry man loves hearing he is part of history.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_katrin_coin_resolve", [
          (main_party_has_troop, "trp_npc11"),
          (eq, "$g_sod_katrin_last_coin_witnessed", 1),
          (eq, "$g_sod_katrin_last_coin_confronted", 1),
          (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve The Last Coin in Camp through practical care.",
        [
          (assign, "$g_sod_katrin_last_coin_result_grade", 3),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc11", 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc11"),
          (display_message, "@The camp eats, the sick are tended, and the coin is gone without regret. Katrin calls it ordinary sense, which is her highest poetry.", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_katrin_coin_hard", [
          (main_party_has_troop, "trp_npc11"),
          (eq, "$g_sod_katrin_last_coin_witnessed", 1),
          (eq, "$g_sod_katrin_last_coin_confronted", 1),
          (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve The Last Coin in Camp by accepting heroic waste.",
        [
          (assign, "$g_sod_katrin_last_coin_result_grade", 1),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc11", 0),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc11"),
          (display_message, "@The opportunity pays in noise and risk. Katrin keeps the camp together anyway, but every ladle of thin broth sounds like an accusation.", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_matheld_step_start", [
          (main_party_has_troop, "trp_npc8"),
          (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc8", slot_troop_companion_approval, 45),
        ], "Speak with Matheld about No Backward Step.",
        [
          (troop_set_slot, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Matheld sets her shield near the fire like a second face. 'There are days a company learns whether its back is bone or smoke.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_matheld_step_stand", [
          (main_party_has_troop, "trp_npc8"),
          (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Stand firm and answer the threat directly.",
        [
          (troop_set_slot, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_hard_victory, 2),
          (display_message, "@Matheld bares her teeth. 'Good. Let them see the shield before they feel it.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_matheld_step_temper", [
          (main_party_has_troop, "trp_npc8"),
          (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Temper courage with a plan that saves lives.",
        [
          (troop_set_slot, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc8", 2),
          (display_message, "@Matheld grunts. 'Planning is not cowardice if the shield still faces forward.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_matheld_step_yield", [
          (main_party_has_troop, "trp_npc8"),
          (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Yield ground and avoid the challenge.",
        [
          (troop_set_slot, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_cowardice, 2),
          (display_message, "@Matheld's voice drops. 'Every backward step teaches someone to chase.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_matheld_step_resolve", [
          (main_party_has_troop, "trp_npc8"),
          (eq, "$g_sod_matheld_no_backward_step_witnessed", 1),
          (eq, "$g_sod_matheld_no_backward_step_confronted", 1),
          (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve No Backward Step with courage held in discipline.",
        [
          (assign, "$g_sod_matheld_no_backward_step_result_grade", 3),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc8", 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc8"),
          (display_message, "@The threat breaks against a shield wall that knows when to stand and when to breathe. Matheld calls it courage with teeth.", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_matheld_step_hard", [
          (main_party_has_troop, "trp_npc8"),
          (eq, "$g_sod_matheld_no_backward_step_witnessed", 1),
          (eq, "$g_sod_matheld_no_backward_step_confronted", 1),
          (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve No Backward Step by spending blood for reputation.",
        [
          (assign, "$g_sod_matheld_no_backward_step_result_grade", 1),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc8", 0),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc8"),
          (display_message, "@No one can call the company soft. The dead cannot call it wise. Matheld accepts the courage and says nothing of the cost.", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_alayen_standard_start", [
          (main_party_has_troop, "trp_npc9"),
          (troop_slot_eq, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc9", slot_troop_companion_approval, 45),
        ], "Speak with Alayen about The Standard and the Self.",
        [
          (troop_set_slot, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Alayen folds a strip of worn cloth with formal care. 'A standard is not decoration. It is a promise men die believing.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_alayen_standard_duty", [
          (main_party_has_troop, "trp_npc9"),
          (troop_slot_eq, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Tell Alayen honor means duty to those beneath the banner.",
        [
          (troop_set_slot, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_help_village, 2),
          (display_message, "@Alayen inclines his head. 'Then nobility is not a height. It is a weight. Good.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_alayen_standard_oath", [
          (main_party_has_troop, "trp_npc9"),
          (troop_slot_eq, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Keep the public oath even at real cost.",
        [
          (troop_set_slot, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc9", 4),
          (display_message, "@Alayen's expression steadies. 'Cost is where oath becomes more than speech.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_alayen_standard_pride", [
          (main_party_has_troop, "trp_npc9"),
          (troop_slot_eq, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Use the standard to secure prestige and obedience.",
        [
          (troop_set_slot, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc9", -4),
          (display_message, "@Alayen goes very still. 'A banner used as ornament soon becomes a rag.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_alayen_standard_resolve", [
          (main_party_has_troop, "trp_npc9"),
          (troop_slot_eq, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve The Standard and the Self through responsibility.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc9", 1),
          (display_message, "@The promise is kept where all can see it. Alayen lowers the standard only after the last dependent is safe.", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_alayen_standard_hard", [
          (main_party_has_troop, "trp_npc9"),
          (troop_slot_eq, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve The Standard and the Self through prestige.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc9", 0),
          (display_message, "@The company looks grander for it. Alayen remains, but he watches the standard as if checking whether it still means anything.", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_nizar_charge_start", [
          (main_party_has_troop, "trp_npc13"),
          (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc13", slot_troop_companion_approval, 45),
        ], "Speak with Nizar about The Impossible Charge.",
        [
          (troop_set_slot, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Nizar leans toward the fire as if it were an audience. 'There is a charge men call impossible because they lack imagination. There is also the other kind. I would prefer we learn the difference before dawn.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_nizar_charge_daring", [
          (main_party_has_troop, "trp_npc13"),
          (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Take the daring rescue before the enemy can form.",
        [
          (troop_set_slot, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_hard_victory, 2),
          (display_message, "@Nizar springs up smiling. 'At last, a decision with a pulse. I shall try not to improve it too much when I retell it.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_nizar_charge_responsible", [
          (main_party_has_troop, "trp_npc13"),
          (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Make the charge work by planning the way out first.",
        [
          (troop_set_slot, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc13", 2),
          (display_message, "@Nizar makes a face, then laughs. 'A cautious legend. Disgraceful. Useful. Possibly immortal.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_nizar_charge_refuse", [
          (main_party_has_troop, "trp_npc13"),
          (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Refuse the charge as needless theater.",
        [
          (troop_set_slot, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_cowardice, 1),
          (display_message, "@Nizar bows too deeply. 'Of course. We shall leave the impossible to poorer poets.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_nizar_charge_resolve", [
          (main_party_has_troop, "trp_npc13"),
          (eq, "$g_sod_nizar_charge_witnessed", 1),
          (eq, "$g_sod_nizar_charge_confronted", 1),
          (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve The Impossible Charge with glory and survivors.",
        [
          (assign, "$g_sod_nizar_charge_result_grade", 3),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc13", 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc13"),
          (display_message, "@The charge breaks the enemy and brings the living home. Nizar raises a cup. 'A rare triumph: the song need not lie about the ending.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_nizar_charge_hard", [
          (main_party_has_troop, "trp_npc13"),
          (eq, "$g_sod_nizar_charge_witnessed", 1),
          (eq, "$g_sod_nizar_charge_confronted", 1),
          (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve The Impossible Charge by spending blood for legend.",
        [
          (assign, "$g_sod_nizar_charge_result_grade", 1),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc13", 0),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc13"),
          (display_message, "@The story will travel farther than the burial count. Nizar still smiles, but the smile arrives late. 'Yes. That is one way to become unforgettable.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_lezalit_discipline_start", [
          (main_party_has_troop, "trp_npc14"),
          (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc14", slot_troop_companion_approval, 45),
        ], "Speak with Lezalit about Discipline Without Chains.",
        [
          (troop_set_slot, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Lezalit watches the drill line until one man drops his shield from exhaustion. 'There. That is the moment command decides whether it trains soldiers or breaks them.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_lezalit_discipline_reform", [
          (main_party_has_troop, "trp_npc14"),
          (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Order Lezalit to reform the drills without softening standards.",
        [
          (troop_set_slot, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_train_troops, 3),
          (display_message, "@Lezalit studies you for a long moment. 'Good. Mercy that preserves standards is not weakness. It is efficiency with a conscience.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_lezalit_discipline_punish", [
          (main_party_has_troop, "trp_npc14"),
          (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Back harsh punishment to restore order.",
        [
          (troop_set_slot, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc14", 2),
          (display_message, "@Lezalit nods once. 'The line will hold. Whether it learns why is another matter.'", 0xCCCC66),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_lezalit_discipline_dismiss", [
          (main_party_has_troop, "trp_npc14"),
          (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Tell Lezalit the men need less discipline, not more.",
        [
          (call_script, "script_sod_companion_shift_approval", "trp_npc14", -5),
          (display_message, "@Lezalit's expression closes like a gate. 'Then pray sentiment can hold a shield wall.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_lezalit_discipline_resolve", [
          (main_party_has_troop, "trp_npc14"),
          (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve Discipline Without Chains through reform.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc14", 1),
          (display_message, "@The drills remain hard, but the men understand them now. Lezalit calls it obedience. Later, more quietly, he calls it command.", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_lezalit_discipline_hard", [
          (main_party_has_troop, "trp_npc14"),
          (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve Discipline Without Chains through fear.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc14", 0),
          (display_message, "@The line becomes quiet and fast to obey. Lezalit approves of the order, but even he does not call it loyalty.", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_artimenner_siege_start", [
          (main_party_has_troop, "trp_npc15"),
          (troop_slot_eq, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc15", slot_troop_companion_approval, 45),
        ], "Speak with Artimenner about The Siege That Should Have Worked.",
        [
          (troop_set_slot, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Artimenner lays three little sticks into a wall shape, then knocks one loose. 'This is how men die: not from courage, but from one brace nobody inspected.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_artimenner_siege_prepare", [
          (main_party_has_troop, "trp_npc15"),
          (troop_slot_eq, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Give Artimenner time and materials to rebuild the works properly.",
        [
          (troop_set_slot, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_orderly_profit, 2),
          (display_message, "@Artimenner blinks, as if bracing for argument that never comes. 'Good. Remarkable. We may yet defeat gravity and stupidity in the same week.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_artimenner_siege_improvise", [
          (main_party_has_troop, "trp_npc15"),
          (troop_slot_eq, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Ask him to improvise a leaner plan with what the army has.",
        [
          (troop_set_slot, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc15", 2),
          (display_message, "@Artimenner pinches the bridge of his nose. 'Inferior, but possible. I prefer possible to glorious nonsense.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_artimenner_siege_blame", [
          (main_party_has_troop, "trp_npc15"),
          (troop_slot_eq, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Tell Artimenner he will be blamed if the works fail.",
        [
          (troop_set_slot, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc15", -6),
          (display_message, "@Artimenner's voice goes flat. 'Ah. So I am not an engineer. I am a bucket for falling stones.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_artimenner_siege_resolve", [
          (main_party_has_troop, "trp_npc15"),
          (troop_slot_eq, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve The Siege That Should Have Worked by respecting the design.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc15", 1),
          (display_message, "@The works hold because they were built to hold. Artimenner allows himself one grim smile. 'At last. A wall that understands its vocation.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_artimenner_siege_hard", [
          (main_party_has_troop, "trp_npc15"),
          (troop_slot_eq, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve The Siege That Should Have Worked by shifting blame.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc15", 0),
          (display_message, "@The failed work finds a culprit and the army moves on. Artimenner does not. 'There. A neat report. Shame it cannot carry a ladder.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_deshavi_tracks_start", [
          (main_party_has_troop, "trp_npc7"),
          (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc7", slot_troop_companion_approval, 45),
        ], "Speak with Deshavi about Tracks Through Ash.",
        [
          (troop_set_slot, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Deshavi lays three blackened twigs by the fire. 'Same ash on all of them. Three villages. Same riders passed before the smoke.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_deshavi_tracks_rescue", [
          (main_party_has_troop, "trp_npc7"),
          (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Follow Deshavi's trail to rescue survivors.",
        [
          (troop_set_slot, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_food_security, 3),
          (display_message, "@Deshavi nods without smiling. 'Good. Poor folk leave signs because rich men do not leave help.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_deshavi_tracks_ambush", [
          (main_party_has_troop, "trp_npc7"),
          (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Use the trail to ambush the raiders first.",
        [
          (troop_set_slot, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_safe_roadcraft, 2),
          (display_message, "@Deshavi checks her bowstring. 'Better to find wolves before they find doors.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_deshavi_tracks_ignore", [
          (main_party_has_troop, "trp_npc7"),
          (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Tell Deshavi the company cannot chase every burned trail.",
        [
          (call_script, "script_sod_companion_shift_approval", "trp_npc7", -5),
          (display_message, "@Deshavi gathers the twigs back into her palm. 'No. Only the trails poor enough to be quiet.'", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_deshavi_tracks_resolve", [
          (main_party_has_troop, "trp_npc7"),
          (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve Tracks Through Ash by sheltering survivors.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc7", 1),
          (display_message, "@The survivors are fed, hidden, and guided toward safer ground. Deshavi only says, 'They will remember who looked down and saw tracks.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_deshavi_tracks_hard", [
          (main_party_has_troop, "trp_npc7"),
          (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve Tracks Through Ash by hunting the raiders only.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc7", 0),
          (display_message, "@The raiders bleed for the ash they left behind. Deshavi accepts the dead, but not the ones you did not stop to count.", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_klethi_knife_start", [
          (main_party_has_troop, "trp_npc16"),
          (troop_slot_eq, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_none),
          (troop_slot_ge, "trp_npc16", slot_troop_companion_approval, 45),
        ], "Speak with Klethi about A Knife With a Name.",
        [
          (troop_set_slot, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (display_message, "@Klethi turns a small knife in her fingers without looking at it. 'Funny thing. A blade can go nameless for years, then one old face remembers it.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_klethi_knife_protect", [
          (main_party_has_troop, "trp_npc16"),
          (troop_slot_eq, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Protect Klethi from the old accusation.",
        [
          (troop_set_slot, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_stealth_success, 3),
          (display_message, "@Klethi's smile almost reaches her eyes. 'Careful. Protecting thieves is how honest people learn useful habits.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_klethi_knife_face", [
          (main_party_has_troop, "trp_npc16"),
          (troop_slot_eq, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Make Klethi face the damage, but on her own terms.",
        [
          (troop_set_slot, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_shift_approval", "trp_npc16", 2),
          (display_message, "@Klethi pockets the knife. 'My terms, then. That is the part people forget when they say justice.'", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_klethi_knife_sellout", [
          (main_party_has_troop, "trp_npc16"),
          (troop_slot_eq, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
        ], "Trade Klethi's old secret for leverage.",
        [
          (troop_set_slot, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_betray_autonomy, 2),
          (display_message, "@Klethi laughs once. Small sound. No warmth. 'There it is. Belonging with a price tag.'", 0xCC6666),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_klethi_knife_resolve", [
          (main_party_has_troop, "trp_npc16"),
          (troop_slot_eq, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve A Knife With a Name by letting Klethi choose.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc16", 1),
          (display_message, "@Klethi handles the old debt quietly and returns before dawn. 'Still here,' she says. For her, it is a long speech.", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_klethi_knife_hard", [
          (main_party_has_troop, "trp_npc16"),
          (troop_slot_eq, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Resolve A Knife With a Name by using the secret.",
        [
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc16", 0),
          (display_message, "@The secret buys leverage. Klethi buys distance. She stays, but every door near her seems half open now.", 0xCC9966),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_acknowledge_warnings", [
          (assign, ":has_pending_warning", 0),
          (try_for_range, ":companion", companions_begin, companions_end),
            (main_party_has_troop, ":companion"),
            (troop_slot_eq, ":companion", slot_troop_companion_warning_state, sod_companion_warning_pending),
            (assign, ":has_pending_warning", 1),
          (try_end),
          (eq, ":has_pending_warning", 1),
        ], "Hold the fire open for grievances.",
        [
          (try_for_range, ":companion", companions_begin, companions_end),
            (main_party_has_troop, ":companion"),
            (troop_slot_eq, ":companion", slot_troop_companion_warning_state, sod_companion_warning_pending),
            (call_script, "script_sod_companion_warning_to_s0", ":companion"),
            (display_message, "@{s0}", 0xCC9966),
            (troop_set_slot, ":companion", slot_troop_companion_warning_state, sod_companion_warning_acknowledged),
            (call_script, "script_sod_companion_shift_approval", ":companion", 3),
          (try_end),
          (display_message, "@The company hears itself speak plainly. Some wounds are named before they split open.", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_repair_acknowledged_warnings", [
          (assign, ":has_named_warning", 0),
          (try_for_range, ":companion", companions_begin, companions_end),
            (main_party_has_troop, ":companion"),
            (this_or_next|troop_slot_eq, ":companion", slot_troop_companion_warning_state, sod_companion_warning_final),
            (troop_slot_eq, ":companion", slot_troop_companion_warning_state, sod_companion_warning_acknowledged),
            (troop_get_slot, ":approval", ":companion", slot_troop_companion_approval),
            (lt, ":approval", 45),
            (assign, ":has_named_warning", 1),
          (try_end),
          (eq, ":has_named_warning", 1),
        ], "Make amends for named grievances.",
        [
          (try_for_range, ":companion", companions_begin, companions_end),
            (main_party_has_troop, ":companion"),
            (this_or_next|troop_slot_eq, ":companion", slot_troop_companion_warning_state, sod_companion_warning_final),
            (troop_slot_eq, ":companion", slot_troop_companion_warning_state, sod_companion_warning_acknowledged),
            (troop_get_slot, ":approval", ":companion", slot_troop_companion_approval),
            (lt, ":approval", 45),
            (call_script, "script_sod_companion_shift_approval", ":companion", 8),
            (call_script, "script_sod_companion_reconciliation_to_s0", ":companion"),
            (display_message, "@{s0}", 0x99CCFF),
            (troop_set_slot, ":companion", slot_troop_companion_warning_state, sod_companion_warning_acknowledged),
          (try_end),
          (display_message, "@Promises are made in plain language tonight. They will need deeds later, but the worst silences have loosened.", 0x99CCFF),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_campfire_back", [], "Bank the fire and return.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),
]
