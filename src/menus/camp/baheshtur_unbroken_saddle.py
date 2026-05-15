MENUS = [
("baheshtur_unbroken_saddle", mnf_scale_picture|mnf_enable_hot_keys,
   "Baheshtur stands among captured tack, loose arrows, and riderless horses. The living witness has spoken, and the rider oath trial has shown what the beaten men do when fear has teeth.^^{reg1?The horde camp is broken, and many riders have nowhere to return.:The raider band is broken, and the survivors are waiting to learn whether defeat means a new master.} Baheshtur keeps one hand on a saddle strap. A road chosen can be hard and still be free.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (try_begin),
        (this_or_next|neg|main_party_has_troop, "trp_npc5"),
        (neq, "$g_sod_baheshtur_saddle_pending", 1),
        (assign, "$g_sod_baheshtur_saddle_pending", 0),
        (assign, "$g_sod_baheshtur_saddle_cause", 0),
        (assign, "$g_sod_baheshtur_saddle_witnessed", 0),
        (assign, "$g_sod_baheshtur_saddle_confronted", 0),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (this_or_next|neq, "$g_sod_baheshtur_saddle_witnessed", 1),
        (neq, "$g_sod_baheshtur_saddle_confronted", 1),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (eq, "$g_sod_baheshtur_saddle_cause", 2),
        (assign, reg1, 1),
      (else_try),
        (assign, reg1, 0),
      (try_end),
    ],
    [
      ("baheshtur_saddle_free", [
          (main_party_has_troop, "trp_npc5"),
          (eq, "$g_sod_baheshtur_saddle_pending", 1),
          (eq, "$g_sod_baheshtur_saddle_witnessed", 1),
          (eq, "$g_sod_baheshtur_saddle_confronted", 1),
        ], "Offer honorable freedom to riders who swear freely.",
        [
          (assign, "$g_sod_baheshtur_saddle_pending", 0),
          (assign, "$g_sod_baheshtur_saddle_result_grade", 3),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_black_khergit_camp_defeat, 2),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc5", 1),
          (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_metadata, "$g_sod_baheshtur_saddle_result_grade"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc5"),
          (call_script, "script_sod_companion_baheshtur_apply_saddle_payoff"),
          (display_message, "@The riders who remain do so by their own word. The Unbroken Saddle remembers chosen loyalty.", 0x99CCFF),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("baheshtur_saddle_pursuit", [
          (main_party_has_troop, "trp_npc5"),
          (eq, "$g_sod_baheshtur_saddle_pending", 1),
          (eq, "$g_sod_baheshtur_saddle_witnessed", 1),
          (eq, "$g_sod_baheshtur_saddle_confronted", 1),
        ], "Ride hard after the raiders, but leave surrender unchained.",
        [
          (assign, "$g_sod_baheshtur_saddle_pending", 0),
          (try_begin),
            (lt, "$g_sod_baheshtur_saddle_result_grade", 2),
            (assign, "$g_sod_baheshtur_saddle_result_grade", 2),
          (try_end),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_safe_roadcraft, 2),
          (call_script, "script_sod_companion_shift_approval", "trp_npc5", 2),
          (try_begin),
            (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
            (troop_set_slot, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (else_try),
            (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
            (call_script, "script_sod_companion_advance_personal_quest", "trp_npc5", 1),
            (call_script, "script_sod_companion_baheshtur_apply_saddle_payoff"),
          (try_end),
          (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_metadata, "$g_sod_baheshtur_saddle_result_grade"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc5"),
          (display_message, "@Baheshtur drives the pursuit without turning surrender into rope. Respect follows hard behind the horses.", 0xCCCC66),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("baheshtur_saddle_submission", [
          (main_party_has_troop, "trp_npc5"),
          (eq, "$g_sod_baheshtur_saddle_pending", 1),
          (eq, "$g_sod_baheshtur_saddle_witnessed", 1),
          (eq, "$g_sod_baheshtur_saddle_confronted", 1),
        ], "Force submission. Broken riders are useful riders.",
        [
          (assign, "$g_sod_baheshtur_saddle_pending", 0),
          (assign, "$g_sod_baheshtur_saddle_result_grade", 1),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc5", 0),
          (troop_set_slot, "trp_npc5", slot_troop_companion_warning_state, sod_companion_warning_pending),
          (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_metadata, "$g_sod_baheshtur_saddle_result_grade"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc5"),
          (display_message, "@The riders obey. Baheshtur does not mistake obedience for loyalty.", 0xCC6666),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("baheshtur_saddle_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("baheshtur_rider_oath_trial", mnf_scale_picture|mnf_enable_hot_keys,
   "The witness waits with the other beaten riders beyond the camp smoke. Baheshtur marks a line in the dust with one boot heel. 'A man who crosses this line by choice rides free. A man dragged over it is still a prisoner.'^^Some riders want the road. Some want revenge. The oath will be tested before the company, not hidden inside a menu of orders.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("baheshtur_trial_free_oath", [
          (main_party_has_troop, "trp_npc5"),
          (eq, "$g_sod_baheshtur_saddle_pending", 1),
          (eq, "$g_sod_baheshtur_saddle_witnessed", 1),
          (eq, "$g_sod_baheshtur_saddle_confronted", 0),
        ], "Let Baheshtur ask for a free oath in front of armed riders.",
        [
          (assign, "$g_sod_baheshtur_saddle_confronted", 1),
          (assign, "$g_sod_baheshtur_saddle_result_grade", 3),
          (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_metadata, "$g_sod_baheshtur_saddle_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc5", 3),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc5"),
          (display_message, "@Baheshtur lets silence work. One rider crosses the line, then another. The oath holds because no hand drags it.", 0x99CCFF),
          (start_map_conversation, "trp_npc5"),
        ]
      ),
      ("baheshtur_trial_defend_line", [
          (main_party_has_troop, "trp_npc5"),
          (eq, "$g_sod_baheshtur_saddle_pending", 1),
          (eq, "$g_sod_baheshtur_saddle_witnessed", 1),
          (eq, "$g_sod_baheshtur_saddle_confronted", 0),
        ], "Stand with Baheshtur when the oath turns violent.",
        [
          (modify_visitors_at_site, "scn_random_scene"),
          (reset_visitors),
          (set_visitor, 0, "trp_player"),
          (set_visitor, 1, "trp_npc5"),
          (set_visitor, 2, "trp_watchman"),
          (set_visitor, 10, "trp_black_khergit_horseman"),
          (set_visitor, 11, "trp_black_khergit_guard"),
          (set_visitor, 12, "trp_black_khergit_horseman"),
          (set_jump_mission, "mt_companion_baheshtur_rider_oath"),
          (jump_to_scene, "scn_random_scene"),
          (change_screen_mission),
        ]
      ),
      ("baheshtur_trial_bind", [
          (main_party_has_troop, "trp_npc5"),
          (eq, "$g_sod_baheshtur_saddle_pending", 1),
          (eq, "$g_sod_baheshtur_saddle_witnessed", 1),
          (eq, "$g_sod_baheshtur_saddle_confronted", 0),
        ], "Bind the riders first and call obedience peace.",
        [
          (assign, "$g_sod_baheshtur_saddle_confronted", 1),
          (assign, "$g_sod_baheshtur_saddle_result_grade", 1),
          (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_metadata, "$g_sod_baheshtur_saddle_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc5", -3),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc5"),
          (display_message, "@The line is quiet because no one can move. Baheshtur watches the bound riders and says nothing.", 0xCC9966),
          (start_map_conversation, "trp_npc5"),
        ]
      ),
      ("baheshtur_trial_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("baheshtur_rider_oath_succeeded", mnf_scale_picture|mnf_enable_hot_keys,
   "The dust settles around men who had to choose while blades were already drawn. Baheshtur lowers his weapon first, and the witness crosses the line with his hands open.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_baheshtur_saddle_confronted", 1),
      (try_begin),
        (le, "$g_sod_baheshtur_saddle_result_grade", 0),
        (assign, "$g_sod_baheshtur_saddle_result_grade", 2),
      (try_end),
      (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_metadata, "$g_sod_baheshtur_saddle_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc5"),
    ],
    [
      ("baheshtur_rider_oath_after", [], "Settle the oath with Baheshtur.",
        [
          (start_map_conversation, "trp_npc5"),
        ]
      ),
    ]
  ),

("baheshtur_rider_oath_failed", mnf_scale_picture|mnf_enable_hot_keys,
   "The oath trial breaks ugly. The riders survive enough to remember fear, and Baheshtur survives enough to hate how close freedom came to looking like a trap.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_baheshtur_saddle_confronted", 1),
      (assign, "$g_sod_baheshtur_saddle_result_grade", -1),
      (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_metadata, "$g_sod_baheshtur_saddle_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc5"),
    ],
    [
      ("baheshtur_rider_oath_failed_after", [], "Face Baheshtur after the broken oath.",
        [
          (start_map_conversation, "trp_npc5"),
        ]
      ),
    ]
  ),
]
