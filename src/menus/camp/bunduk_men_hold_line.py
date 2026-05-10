MENUS = [
("bunduk_men_hold_line", mnf_scale_picture|mnf_enable_hot_keys,
   "Bunduk waits near the cookfires with men who have stopped pretending not to listen. {s1}^^The ranker has spoken and the line has been tested under pressure. Bunduk watches whether command changes after the men prove what they have been carrying.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (try_begin),
        (this_or_next|neg|main_party_has_troop, "trp_npc10"),
        (neq, "$g_sod_bunduk_line_pending", 1),
        (assign, "$g_sod_bunduk_line_pending", 0),
        (assign, "$g_sod_bunduk_line_cause", 0),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (eq, "$g_sod_bunduk_line_cause", 2),
        (str_store_string, s1, "@Some are short pay, and all of them know an empty purse can sound a lot like an officer's promise."),
      (else_try),
        (str_store_string, s1, "@Some are short friends after the last fight, and all of them know when officers call waste discipline."),
      (try_end),
    ],
    [
      ("bunduk_line_advocate", [
          (main_party_has_troop, "trp_npc10"),
          (eq, "$g_sod_bunduk_line_pending", 1),
          (eq, "$g_sod_bunduk_line_witnessed", 1),
          (eq, "$g_sod_bunduk_line_confronted", 1),
        ], "Back Bunduk. Fix watches, stores, pay, and stupid orders.",
        [
          (assign, "$g_sod_bunduk_line_pending", 0),
          (assign, "$g_sod_bunduk_line_result_grade", 3),
          (quest_set_slot, "qst_companion_bunduk_men_hold_line", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_bunduk_men_hold_line", slot_quest_sod_runtime_metadata, "$g_sod_bunduk_line_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_food_security, 3),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_train_troops, 2),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc10", 1),
          (call_script, "script_sod_companion_bunduk_apply_line_payoff"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc10"),
          (display_message, "@The line gets better watches, fairer stores, and orders worth obeying. Bunduk calls it common sense, which from him is almost poetry.", 0x99CCFF),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("bunduk_line_compromise", [
          (main_party_has_troop, "trp_npc10"),
          (eq, "$g_sod_bunduk_line_pending", 1),
          (eq, "$g_sod_bunduk_line_witnessed", 1),
          (eq, "$g_sod_bunduk_line_confronted", 1),
        ], "Make a practical compromise. Some complaints wait until after the campaign.",
        [
          (assign, "$g_sod_bunduk_line_pending", 0),
          (assign, "$g_sod_bunduk_line_result_grade", 2),
          (quest_set_slot, "qst_companion_bunduk_men_hold_line", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_bunduk_men_hold_line", slot_quest_sod_runtime_metadata, "$g_sod_bunduk_line_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_food_security, 1),
          (call_script, "script_sod_companion_shift_approval", "trp_npc10", -2),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc10", 0),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc10"),
          (display_message, "@Bunduk accepts the compromise, but not warmly. 'Campaigns always need one more week from the men who already paid.'", 0xCC9966),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("bunduk_line_crackdown", [
          (main_party_has_troop, "trp_npc10"),
          (eq, "$g_sod_bunduk_line_pending", 1),
          (eq, "$g_sod_bunduk_line_witnessed", 1),
          (eq, "$g_sod_bunduk_line_confronted", 1),
        ], "Enforce command authority. The line obeys first and complains later.",
        [
          (assign, "$g_sod_bunduk_line_pending", 0),
          (assign, "$g_sod_bunduk_line_result_grade", 1),
          (quest_set_slot, "qst_companion_bunduk_men_hold_line", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_bunduk_men_hold_line", slot_quest_sod_runtime_metadata, "$g_sod_bunduk_line_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_lezalit_ief_harsh, 2),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc10", 0),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc10"),
          (troop_set_slot, "trp_npc10", slot_troop_companion_warning_state, sod_companion_warning_pending),
          (display_message, "@The line obeys. Bunduk stays with it, but his salute looks like something nailed to a door.", 0xCC6666),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("bunduk_line_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("bunduk_line_test", mnf_scale_picture|mnf_enable_hot_keys,
   "Bunduk lays out the complaint as a watch bill, not a speech. Thin stores here. Dead men still on the old roster there. A night line so tired it would break before the enemy touched it.^^Then horns sound from the dark edge of camp. Bunduk only says, 'There. Now command gets to learn fast.'",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("bunduk_line_test_defend", [
          (main_party_has_troop, "trp_npc10"),
          (eq, "$g_sod_bunduk_line_pending", 1),
          (eq, "$g_sod_bunduk_line_witnessed", 1),
          (eq, "$g_sod_bunduk_line_confronted", 0),
        ], "Stand the tired line with Bunduk.",
        [
          (modify_visitors_at_site, "scn_random_scene"),
          (reset_visitors),
          (set_visitor, 0, "trp_player"),
          (set_visitor, 1, "trp_npc10"),
          (set_visitor, 2, "trp_watchman"),
          (set_visitor, 3, "trp_caravan_guard"),
          (set_visitor, 10, "trp_bandit"),
          (set_visitor, 11, "trp_brigand"),
          (set_visitor, 12, "trp_henchman"),
          (set_jump_mission, "mt_companion_bunduk_line_test"),
          (jump_to_scene, "scn_random_scene"),
          (change_screen_mission),
        ]
      ),
      ("bunduk_line_test_reassign", [
          (main_party_has_troop, "trp_npc10"),
          (eq, "$g_sod_bunduk_line_pending", 1),
          (eq, "$g_sod_bunduk_line_witnessed", 1),
          (eq, "$g_sod_bunduk_line_confronted", 0),
        ], "Rework the watches before the attack lands.",
        [
          (assign, "$g_sod_bunduk_line_confronted", 1),
          (assign, "$g_sod_bunduk_line_result_grade", 2),
          (quest_set_slot, "qst_companion_bunduk_men_hold_line", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_bunduk_men_hold_line", slot_quest_sod_runtime_metadata, "$g_sod_bunduk_line_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_train_troops, 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc10"),
          (display_message, "@The attack finds a line awake enough to answer. Bunduk marks the watch bill with a grunt that is almost approval.", 0xCCCC66),
          (jump_to_menu, "mnu_bunduk_men_hold_line"),
        ]
      ),
      ("bunduk_line_test_drive", [
          (main_party_has_troop, "trp_npc10"),
          (eq, "$g_sod_bunduk_line_pending", 1),
          (eq, "$g_sod_bunduk_line_witnessed", 1),
          (eq, "$g_sod_bunduk_line_confronted", 0),
        ], "Drive the tired line harder. They can rest after obedience.",
        [
          (assign, "$g_sod_bunduk_line_confronted", 1),
          (assign, "$g_sod_bunduk_line_result_grade", 1),
          (quest_set_slot, "qst_companion_bunduk_men_hold_line", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_bunduk_men_hold_line", slot_quest_sod_runtime_metadata, "$g_sod_bunduk_line_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_lezalit_ief_harsh, 1),
          (call_script, "script_sod_companion_shift_approval", "trp_npc10", -2),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc10"),
          (display_message, "@The line holds because it must. Bunduk counts the cost before anyone counts the victory.", 0xCC9966),
          (jump_to_menu, "mnu_bunduk_men_hold_line"),
        ]
      ),
      ("bunduk_line_test_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("bunduk_line_test_succeeded", mnf_scale_picture|mnf_enable_hot_keys,
   "The night attack breaks on a line that finally had enough warning, bolts, and men standing where the roster claimed they stood. Bunduk looks down the row of common soldiers before he looks at you.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_bunduk_line_confronted", 1),
      (try_begin),
        (le, "$g_sod_bunduk_line_result_grade", 0),
        (assign, "$g_sod_bunduk_line_result_grade", 3),
      (try_end),
      (quest_set_slot, "qst_companion_bunduk_men_hold_line", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_bunduk_men_hold_line", slot_quest_sod_runtime_metadata, "$g_sod_bunduk_line_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc10"),
    ],
    [
      ("bunduk_line_after", [], "Speak with Bunduk about the line.",
        [
          (jump_to_menu, "mnu_bunduk_men_hold_line"),
        ]
      ),
    ]
  ),

("bunduk_line_test_failed", mnf_scale_picture|mnf_enable_hot_keys,
   "The line holds badly: gaps closed by luck, curses, and men too tired to run. Bunduk pulls survivors back into order with a voice rough enough to cut cloth.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_bunduk_line_confronted", 1),
      (assign, "$g_sod_bunduk_line_result_grade", -1),
      (quest_set_slot, "qst_companion_bunduk_men_hold_line", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_bunduk_men_hold_line", slot_quest_sod_runtime_metadata, "$g_sod_bunduk_line_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc10"),
    ],
    [
      ("bunduk_line_failed_after", [], "Face Bunduk's report.",
        [
          (jump_to_menu, "mnu_bunduk_men_hold_line"),
        ]
      ),
    ]
  ),
]
