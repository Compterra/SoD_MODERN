MENUS = [
("matheld_no_backward_step", mnf_scale_picture|mnf_enable_hot_keys,
   "Matheld plants her shield in the dirt hard enough to make the nearest recruits look up. The battle is over, but the line is still being judged: who held, who ran, who died bravely, and who died because someone mistook noise for courage.^^{reg1?Too many fell while the line stood.:The line gave ground, and fear learned the shape of retreat.} Matheld does not soften the question. What will the next line learn?",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (try_begin),
        (this_or_next|neg|main_party_has_troop, "trp_npc8"),
        (neq, "$g_sod_matheld_no_backward_step_pending", 1),
        (assign, "$g_sod_matheld_no_backward_step_pending", 0),
        (assign, "$g_sod_matheld_no_backward_step_cause", 0),
        (assign, "$g_sod_matheld_no_backward_step_witnessed", 0),
        (assign, "$g_sod_matheld_no_backward_step_confronted", 0),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (this_or_next|neq, "$g_sod_matheld_no_backward_step_witnessed", 1),
        (neq, "$g_sod_matheld_no_backward_step_confronted", 1),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (eq, "$g_sod_matheld_no_backward_step_cause", 2),
        (assign, reg1, 1),
      (else_try),
        (assign, reg1, 0),
      (try_end),
    ],
    [
      ("matheld_step_temper", [
          (main_party_has_troop, "trp_npc8"),
          (eq, "$g_sod_matheld_no_backward_step_pending", 1),
          (eq, "$g_sod_matheld_no_backward_step_witnessed", 1),
          (eq, "$g_sod_matheld_no_backward_step_confronted", 1),
        ], "Temper courage into a shield wall that saves lives.",
        [
          (assign, "$g_sod_matheld_no_backward_step_pending", 0),
          (assign, "$g_sod_matheld_no_backward_step_result_grade", 3),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_honorable_peace, 2),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc8", 1),
          (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_metadata, "$g_sod_matheld_no_backward_step_result_grade"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc8"),
          (call_script, "script_sod_companion_matheld_apply_step_payoff"),
          (display_message, "@Matheld accepts discipline because the shield still faces forward. No Backward Step remembers courage with teeth.", 0x99CCFF),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("matheld_step_stand", [
          (main_party_has_troop, "trp_npc8"),
          (eq, "$g_sod_matheld_no_backward_step_pending", 1),
          (eq, "$g_sod_matheld_no_backward_step_witnessed", 1),
          (eq, "$g_sod_matheld_no_backward_step_confronted", 1),
        ], "Stand firm and answer the next threat directly.",
        [
          (assign, "$g_sod_matheld_no_backward_step_pending", 0),
          (try_begin),
            (lt, "$g_sod_matheld_no_backward_step_result_grade", 2),
            (assign, "$g_sod_matheld_no_backward_step_result_grade", 2),
          (try_end),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_hard_victory, 2),
          (call_script, "script_sod_companion_shift_approval", "trp_npc8", 2),
          (try_begin),
            (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
            (troop_set_slot, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (else_try),
            (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
            (call_script, "script_sod_companion_advance_personal_quest", "trp_npc8", 1),
            (call_script, "script_sod_companion_matheld_apply_step_payoff"),
          (try_end),
          (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_metadata, "$g_sod_matheld_no_backward_step_result_grade"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc8"),
          (display_message, "@Matheld bares her teeth. Let them see the shield before they feel it.", 0xCCCC66),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("matheld_step_blood_price", [
          (main_party_has_troop, "trp_npc8"),
          (eq, "$g_sod_matheld_no_backward_step_pending", 1),
          (eq, "$g_sod_matheld_no_backward_step_witnessed", 1),
          (eq, "$g_sod_matheld_no_backward_step_confronted", 1),
        ], "Make every insult cost blood. No one calls the company soft.",
        [
          (assign, "$g_sod_matheld_no_backward_step_pending", 0),
          (assign, "$g_sod_matheld_no_backward_step_result_grade", 1),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc8", 0),
          (troop_set_slot, "trp_npc8", slot_troop_companion_warning_state, sod_companion_warning_pending),
          (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_metadata, "$g_sod_matheld_no_backward_step_result_grade"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc8"),
          (display_message, "@No one can call the company soft. The dead cannot call it wise.", 0xCC6666),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("matheld_step_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("matheld_shield_line_test", mnf_scale_picture|mnf_enable_hot_keys,
   "The ranker witness gathers three battered shields and two men who still flinch when horns sound behind them. Matheld steps into the line without ceremony. 'Now we find whether courage can breathe.'^^The next lesson will not be argued in camp. It will be felt through wood, mud, and the moment feet want to run.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("matheld_test_breathing_wall", [
          (main_party_has_troop, "trp_npc8"),
          (eq, "$g_sod_matheld_no_backward_step_pending", 1),
          (eq, "$g_sod_matheld_no_backward_step_witnessed", 1),
          (eq, "$g_sod_matheld_no_backward_step_confronted", 0),
        ], "Drill the line to hold, breathe, and withdraw the wounded.",
        [
          (assign, "$g_sod_matheld_no_backward_step_confronted", 1),
          (assign, "$g_sod_matheld_no_backward_step_result_grade", 3),
          (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_metadata, "$g_sod_matheld_no_backward_step_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc8", 3),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc8"),
          (display_message, "@Matheld hates the slow count until the line holds through it. Courage learns to breathe.", 0x99CCFF),
          (jump_to_menu, "mnu_matheld_no_backward_step"),
        ]
      ),
      ("matheld_test_hold_under_charge", [
          (main_party_has_troop, "trp_npc8"),
          (eq, "$g_sod_matheld_no_backward_step_pending", 1),
          (eq, "$g_sod_matheld_no_backward_step_witnessed", 1),
          (eq, "$g_sod_matheld_no_backward_step_confronted", 0),
        ], "Stand with Matheld when the line is rushed.",
        [
          (modify_visitors_at_site, "scn_random_scene"),
          (reset_visitors),
          (set_visitor, 0, "trp_player"),
          (set_visitor, 1, "trp_npc8"),
          (set_visitor, 2, "trp_watchman"),
          (set_visitor, 3, "trp_veteran_fighter"),
          (set_visitor, 10, "trp_bandit"),
          (set_visitor, 11, "trp_brigand"),
          (set_visitor, 12, "trp_henchman"),
          (set_jump_mission, "mt_companion_matheld_shield_line"),
          (jump_to_scene, "scn_random_scene"),
          (change_screen_mission),
        ]
      ),
      ("matheld_test_blood_roar", [
          (main_party_has_troop, "trp_npc8"),
          (eq, "$g_sod_matheld_no_backward_step_pending", 1),
          (eq, "$g_sod_matheld_no_backward_step_witnessed", 1),
          (eq, "$g_sod_matheld_no_backward_step_confronted", 0),
        ], "Answer fear with a charge before the line learns to breathe.",
        [
          (assign, "$g_sod_matheld_no_backward_step_confronted", 1),
          (assign, "$g_sod_matheld_no_backward_step_result_grade", 1),
          (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_metadata, "$g_sod_matheld_no_backward_step_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc8", -3),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc8"),
          (display_message, "@The charge feels brave. The line cheers, then looks back at the gap where discipline should have stood.", 0xCC9966),
          (jump_to_menu, "mnu_matheld_no_backward_step"),
        ]
      ),
      ("matheld_test_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("matheld_shield_line_succeeded", mnf_scale_picture|mnf_enable_hot_keys,
   "The rush breaks against shields that bend without turning. Matheld is breathing hard enough to spit fire, but the wounded are behind the line and alive enough to curse.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_matheld_no_backward_step_confronted", 1),
      (try_begin),
        (le, "$g_sod_matheld_no_backward_step_result_grade", 0),
        (assign, "$g_sod_matheld_no_backward_step_result_grade", 2),
      (try_end),
      (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_metadata, "$g_sod_matheld_no_backward_step_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc8"),
    ],
    [
      ("matheld_shield_line_after", [], "Settle the shield-line lesson with Matheld.",
        [
          (jump_to_menu, "mnu_matheld_no_backward_step"),
        ]
      ),
    ]
  ),

("matheld_shield_line_failed", mnf_scale_picture|mnf_enable_hot_keys,
   "The rush scatters the lesson into mud. The line survives, but it survives with fear in its elbows and Matheld's jaw clenched around words sharp enough to cut.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_matheld_no_backward_step_confronted", 1),
      (assign, "$g_sod_matheld_no_backward_step_result_grade", -1),
      (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_metadata, "$g_sod_matheld_no_backward_step_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc8"),
    ],
    [
      ("matheld_shield_line_failed_after", [], "Face Matheld after the broken line.",
        [
          (jump_to_menu, "mnu_matheld_no_backward_step"),
        ]
      ),
    ]
  ),
]
