MENUS = [
("alayen_standard_self", mnf_scale_picture|mnf_enable_hot_keys,
   "Alayen has planted the company standard where everyone can see it. {s1}^^A witness has named what the cloth promises, and the public test has shown what that promise costs. Alayen watches the people beneath the banner more closely than the banner itself.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (try_begin),
        (this_or_next|neg|main_party_has_troop, "trp_npc9"),
        (neq, "$g_sod_alayen_standard_pending", 1),
        (assign, "$g_sod_alayen_standard_pending", 0),
        (assign, "$g_sod_alayen_standard_cause", 0),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (eq, "$g_sod_alayen_standard_result_grade", -1),
        (str_store_string, s1, "@The test cost more than pride can decorate. Alayen has counted which names the standard failed to cover."),
      (else_try),
        (eq, "$g_sod_alayen_standard_result_grade", 3),
        (str_store_string, s1, "@The standard held because duty stood where display would have posed."),
      (else_try),
        (eq, "$g_sod_alayen_standard_result_grade", 2),
        (str_store_string, s1, "@The standard held publicly, though it paid more in dignity and coin than anyone applauding will remember."),
      (else_try),
        (eq, "$g_sod_alayen_standard_result_grade", 1),
        (str_store_string, s1, "@The standard commanded obedience. Alayen has not decided whether obedience was the same as honor."),
      (else_try),
        (eq, "$g_sod_alayen_standard_cause", 2),
        (str_store_string, s1, "@The standard was raised after public honor and praise."),
      (else_try),
        (str_store_string, s1, "@The standard was raised over people who needed protection more than ceremony."),
      (try_end),
    ],
    [
      ("alayen_standard_duty", [
          (main_party_has_troop, "trp_npc9"),
          (eq, "$g_sod_alayen_standard_pending", 1),
          (eq, "$g_sod_alayen_standard_witnessed", 1),
          (eq, "$g_sod_alayen_standard_confronted", 1),
        ], "Make the standard a promise to protect those beneath it.",
        [
          (assign, "$g_sod_alayen_standard_pending", 0),
          (assign, "$g_sod_alayen_standard_result_grade", 3),
          (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_metadata, "$g_sod_alayen_standard_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_help_village, 3),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_honorable_peace, 2),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc9", 1),
          (call_script, "script_sod_companion_alayen_apply_standard_payoff"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc9"),
          (display_message, "@Alayen lowers the standard only after the vulnerable are accounted for. The Standard and the Self remembers duty.", 0x99CCFF),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("alayen_standard_oath", [
          (main_party_has_troop, "trp_npc9"),
          (eq, "$g_sod_alayen_standard_pending", 1),
          (eq, "$g_sod_alayen_standard_witnessed", 1),
          (eq, "$g_sod_alayen_standard_confronted", 1),
        ], "Keep the oath publicly, even at a visible cost.",
        [
          (assign, "$g_sod_alayen_standard_pending", 0),
          (try_begin),
            (lt, "$g_sod_alayen_standard_result_grade", 2),
            (assign, "$g_sod_alayen_standard_result_grade", 2),
          (try_end),
          (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_metadata, "$g_sod_alayen_standard_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc9", 3),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc9", 1),
          (call_script, "script_sod_companion_alayen_apply_standard_payoff"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc9"),
          (display_message, "@Alayen accepts the cost without ornament. The oath becomes heavier, and therefore truer.", 0xCCCC66),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("alayen_standard_pride", [
          (main_party_has_troop, "trp_npc9"),
          (eq, "$g_sod_alayen_standard_pending", 1),
          (eq, "$g_sod_alayen_standard_witnessed", 1),
          (eq, "$g_sod_alayen_standard_confronted", 1),
        ], "Use the standard to secure obedience and prestige.",
        [
          (assign, "$g_sod_alayen_standard_pending", 0),
          (assign, "$g_sod_alayen_standard_result_grade", 1),
          (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_metadata, "$g_sod_alayen_standard_result_grade"),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc9", 0),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc9"),
          (troop_set_slot, "trp_npc9", slot_troop_companion_warning_state, sod_companion_warning_pending),
          (display_message, "@The company looks grand beneath the banner. Alayen watches it as if checking whether the cloth has become a rag.", 0xCC6666),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("alayen_standard_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("alayen_standard_test", mnf_scale_picture|mnf_enable_hot_keys,
   "The witness's words spread faster than orders. People gather beneath the standard because now the cloth has been asked to mean something. Then armed men test the promise: not a glorious charge, only frightened dependents, a disputed oath, and enough steel to reveal whether honor protects or performs.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("alayen_test_defend", [
          (main_party_has_troop, "trp_npc9"),
          (eq, "$g_sod_alayen_standard_pending", 1),
          (eq, "$g_sod_alayen_standard_witnessed", 1),
          (eq, "$g_sod_alayen_standard_confronted", 0),
        ], "Stand beneath the standard with Alayen.",
        [
          (modify_visitors_at_site, "scn_random_scene"),
          (reset_visitors),
          (set_visitor, 0, "trp_player"),
          (set_visitor, 1, "trp_npc9"),
          (set_visitor, 2, "trp_watchman"),
          (set_visitor, 3, "trp_farmer"),
          (set_visitor, 10, "trp_bandit"),
          (set_visitor, 11, "trp_brigand"),
          (set_visitor, 12, "trp_henchman"),
          (set_jump_mission, "mt_companion_alayen_standard_test"),
          (jump_to_scene, "scn_random_scene"),
          (change_screen_mission),
        ]
      ),
      ("alayen_test_public_cost", [
          (main_party_has_troop, "trp_npc9"),
          (eq, "$g_sod_alayen_standard_pending", 1),
          (eq, "$g_sod_alayen_standard_witnessed", 1),
          (eq, "$g_sod_alayen_standard_confronted", 0),
          (store_troop_gold, ":gold", "trp_player"),
          (ge, ":gold", 250),
        ], "Pay the public cost of the oath before violence decides it.",
        [
          (assign, "$g_sod_alayen_standard_confronted", 1),
          (assign, "$g_sod_alayen_standard_result_grade", 2),
          (call_script, "script_sod_player_charge_gold", 250),
          (eq, reg1, 1),
          (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_metadata, "$g_sod_alayen_standard_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_honorable_peace, 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc9"),
          (display_message, "@The standard costs coin and pride in front of witnesses. Alayen looks relieved that honor has weight.", 0xCCCC66),
          (start_map_conversation, "trp_npc9"),
        ]
      ),
      ("alayen_test_command_prestige", [
          (main_party_has_troop, "trp_npc9"),
          (eq, "$g_sod_alayen_standard_pending", 1),
          (eq, "$g_sod_alayen_standard_witnessed", 1),
          (eq, "$g_sod_alayen_standard_confronted", 0),
        ], "Make the crowd kneel to the standard before anyone questions it.",
        [
          (assign, "$g_sod_alayen_standard_confronted", 1),
          (assign, "$g_sod_alayen_standard_result_grade", 1),
          (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_metadata, "$g_sod_alayen_standard_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc9", -2),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc9"),
          (display_message, "@The crowd obeys the banner. Alayen sees the obedience and searches for the honor.", 0xCC9966),
          (start_map_conversation, "trp_npc9"),
        ]
      ),
      ("alayen_test_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("alayen_standard_test_succeeded", mnf_scale_picture|mnf_enable_hot_keys,
   "The attackers break against the people standing under the standard. Alayen keeps the cloth upright until the last frightened dependent is clear.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_alayen_standard_confronted", 1),
      (try_begin),
        (le, "$g_sod_alayen_standard_result_grade", 0),
        (assign, "$g_sod_alayen_standard_result_grade", 3),
      (try_end),
      (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_metadata, "$g_sod_alayen_standard_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc9"),
    ],
    [
      ("alayen_standard_after", [], "Settle the oath with Alayen.",
        [
          (start_map_conversation, "trp_npc9"),
        ]
      ),
    ]
  ),

("alayen_standard_test_failed", mnf_scale_picture|mnf_enable_hot_keys,
   "The standard stays upright, but not enough people stayed safe beneath it. Alayen wipes dirt from the cloth with a face too controlled to be calm.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_alayen_standard_confronted", 1),
      (assign, "$g_sod_alayen_standard_result_grade", -1),
      (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_metadata, "$g_sod_alayen_standard_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc9"),
    ],
    [
      ("alayen_standard_failed_after", [], "Face Alayen's standard.",
        [
          (start_map_conversation, "trp_npc9"),
        ]
      ),
    ]
  ),
]
