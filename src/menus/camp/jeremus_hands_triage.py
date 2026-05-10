MENUS = [
("jeremus_hands_triage", mnf_scale_picture|mnf_enable_hot_keys,
   "Jeremus has made a surgery from blankets, shields, and shaking hands. {s1}^^The wounded have spoken, and the infirmary crisis has been faced. Now Jeremus waits for an order that will become habit the next time blood outruns clean cloth.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (try_begin),
        (this_or_next|neg|main_party_has_troop, "trp_npc12"),
        (neq, "$g_sod_jeremus_triage_pending", 1),
        (assign, "$g_sod_jeremus_triage_pending", 0),
        (assign, "$g_sod_jeremus_triage_focus_cause", 0),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (eq, "$g_sod_jeremus_triage_result_grade", -1),
        (str_store_string, s1, "@Some beds were overturned before the wounded could be moved. Jeremus has counted the names twice because once was not punishment enough."),
      (else_try),
        (eq, "$g_sod_jeremus_triage_result_grade", 3),
        (str_store_string, s1, "@The raiders broke before the infirmary did. Even the prisoners know who stood between them and the knives."),
      (else_try),
        (eq, "$g_sod_jeremus_triage_result_grade", 2),
        (str_store_string, s1, "@The infirmary held because you found order before the pressure became panic."),
      (else_try),
        (str_store_string, s1, "@There are too many wounded and too little time. Rank, banner, and usefulness all become temptations when breath is running out."),
      (try_end),
    ],
    [
      ("jeremus_triage_mercy", [
          (main_party_has_troop, "trp_npc12"),
          (eq, "$g_sod_jeremus_triage_pending", 1),
          (eq, "$g_sod_jeremus_triage_witnessed", 1),
          (eq, "$g_sod_jeremus_triage_confronted", 1),
        ], "Treat the helpless and enemy wounded by need, not banner.",
        [
          (assign, "$g_sod_jeremus_triage_pending", 0),
          (assign, "$g_sod_jeremus_triage_result_grade", 3),
          (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_metadata, "$g_sod_jeremus_triage_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_free_captives, 3),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_honorable_peace, 2),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc12", 1),
          (call_script, "script_sod_companion_jeremus_apply_triage_payoff"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc12"),
          (display_message, "@The wounded are sorted without rank deciding who deserves breath. Jeremus looks exhausted, but not defeated.", 0x99CCFF),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("jeremus_triage_hard", [
          (main_party_has_troop, "trp_npc12"),
          (eq, "$g_sod_jeremus_triage_pending", 1),
          (eq, "$g_sod_jeremus_triage_witnessed", 1),
          (eq, "$g_sod_jeremus_triage_confronted", 1),
        ], "Use hard triage. Save those most likely to survive.",
        [
          (assign, "$g_sod_jeremus_triage_pending", 0),
          (try_begin),
            (lt, "$g_sod_jeremus_triage_result_grade", 2),
            (assign, "$g_sod_jeremus_triage_result_grade", 2),
          (try_end),
          (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_metadata, "$g_sod_jeremus_triage_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc12", 1),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc12", 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc12"),
          (display_message, "@Jeremus accepts the cruel arithmetic because it is not cruelty. The living are pulled back from the edge.", 0xCCCC66),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("jeremus_triage_company", [
          (main_party_has_troop, "trp_npc12"),
          (eq, "$g_sod_jeremus_triage_pending", 1),
          (eq, "$g_sod_jeremus_triage_witnessed", 1),
          (eq, "$g_sod_jeremus_triage_confronted", 1),
        ], "Save company strength first. Others wait.",
        [
          (assign, "$g_sod_jeremus_triage_pending", 0),
          (assign, "$g_sod_jeremus_triage_result_grade", 1),
          (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_metadata, "$g_sod_jeremus_triage_result_grade"),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc12", 0),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc12"),
          (troop_set_slot, "trp_npc12", slot_troop_companion_warning_state, sod_companion_warning_pending),
          (display_message, "@The company recovers faster. Jeremus does not argue with the result. He only asks who will heal what the result did to you.", 0xCC6666),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("jeremus_triage_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("jeremus_triage_infirmary", mnf_scale_picture|mnf_enable_hot_keys,
   "The wounded ranker leads you to the blanket-walled infirmary just as a quarrel turns sharp. A few desperate men want the prisoner bandages stripped for their own. Others hear hoofbeats and see raiders coming for the helpless.^^Jeremus has both hands red to the wrist. 'If we decide who counts by who can swing a sword today, we have already lost more than cloth.'",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("jeremus_infirmary_defend", [
          (main_party_has_troop, "trp_npc12"),
          (eq, "$g_sod_jeremus_triage_pending", 1),
          (eq, "$g_sod_jeremus_triage_witnessed", 1),
          (eq, "$g_sod_jeremus_triage_confronted", 0),
        ], "Hold the infirmary with Jeremus.",
        [
          (modify_visitors_at_site, "scn_random_scene"),
          (reset_visitors),
          (set_visitor, 0, "trp_player"),
          (set_visitor, 1, "trp_npc12"),
          (set_visitor, 2, "trp_watchman"),
          (set_visitor, 3, "trp_farmer"),
          (set_visitor, 10, "trp_bandit"),
          (set_visitor, 11, "trp_brigand"),
          (set_visitor, 12, "trp_henchman"),
          (set_jump_mission, "mt_companion_jeremus_infirmary"),
          (jump_to_scene, "scn_random_scene"),
          (change_screen_mission),
        ]
      ),
      ("jeremus_infirmary_reorder", [
          (main_party_has_troop, "trp_npc12"),
          (eq, "$g_sod_jeremus_triage_pending", 1),
          (eq, "$g_sod_jeremus_triage_witnessed", 1),
          (eq, "$g_sod_jeremus_triage_confronted", 0),
        ], "Set guards, sort supplies, and keep the wounded under Jeremus' order.",
        [
          (assign, "$g_sod_jeremus_triage_confronted", 1),
          (assign, "$g_sod_jeremus_triage_result_grade", 2),
          (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_metadata, "$g_sod_jeremus_triage_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_honorable_peace, 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc12"),
          (display_message, "@The infirmary steadies because guards and order arrive before panic does. Jeremus can finally look up from the blood.", 0xCCCC66),
          (jump_to_menu, "mnu_jeremus_hands_triage"),
        ]
      ),
      ("jeremus_infirmary_company_first", [
          (main_party_has_troop, "trp_npc12"),
          (eq, "$g_sod_jeremus_triage_pending", 1),
          (eq, "$g_sod_jeremus_triage_witnessed", 1),
          (eq, "$g_sod_jeremus_triage_confronted", 0),
        ], "Strip the enemy wounded first. The company survives on company cloth.",
        [
          (assign, "$g_sod_jeremus_triage_confronted", 1),
          (assign, "$g_sod_jeremus_triage_result_grade", 1),
          (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_metadata, "$g_sod_jeremus_triage_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc12", -2),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc12"),
          (display_message, "@The company wounded get cloth first. The infirmary quiets, but Jeremus hears the silence around the prisoners.", 0xCC9966),
          (jump_to_menu, "mnu_jeremus_hands_triage"),
        ]
      ),
      ("jeremus_infirmary_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("jeremus_infirmary_succeeded", mnf_scale_picture|mnf_enable_hot_keys,
   "The raiders break before the infirmary does. Jeremus drags a wounded prisoner behind the shield wall with the same furious care he gives your own men.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_jeremus_triage_confronted", 1),
      (try_begin),
        (le, "$g_sod_jeremus_triage_result_grade", 0),
        (assign, "$g_sod_jeremus_triage_result_grade", 3),
      (try_end),
      (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_metadata, "$g_sod_jeremus_triage_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc12"),
    ],
    [
      ("jeremus_infirmary_after", [], "Speak with Jeremus about triage.",
        [
          (jump_to_menu, "mnu_jeremus_hands_triage"),
        ]
      ),
    ]
  ),

("jeremus_infirmary_failed", mnf_scale_picture|mnf_enable_hot_keys,
   "The infirmary survives in pieces. Some wounded are moved. Some are not. Jeremus binds a cut across his own arm only after another man points out the blood is his.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_jeremus_triage_confronted", 1),
      (assign, "$g_sod_jeremus_triage_result_grade", -1),
      (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_jeremus_hands_triage", slot_quest_sod_runtime_metadata, "$g_sod_jeremus_triage_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc12"),
    ],
    [
      ("jeremus_infirmary_failed_after", [], "Face Jeremus' triage order.",
        [
          (jump_to_menu, "mnu_jeremus_hands_triage"),
        ]
      ),
    ]
  ),
]
