MENUS = [
("lezalit_discipline_without_chains", mnf_scale_picture|mnf_enable_hot_keys,
   "Lezalit has gathered notes from the defeated Imperial force: punishments, marches, ration drills, execution schedules, and a dozen small methods for turning fear into obedience. {s1}^^The line has spoken and the drill has been tested. Now Lezalit waits to learn what command means when the old Imperial method is useful and poisonous at once.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (try_begin),
        (this_or_next|neg|main_party_has_troop, "trp_npc14"),
        (neq, "$g_sod_lezalit_ief_discipline_pending", 1),
        (assign, "$g_sod_lezalit_ief_discipline_pending", 0),
        (assign, "$g_sod_lezalit_ief_discipline_focus_cause", 0),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (eq, "$g_sod_lezalit_ief_discipline_result_grade", -1),
        (str_store_string, s1, "@The trial broke formation badly enough that even Lezalit has stopped calling failure useful."),
      (else_try),
        (eq, "$g_sod_lezalit_ief_discipline_result_grade", 3),
        (str_store_string, s1, "@The trial held under attack because the men knew what the hardship bought."),
      (else_try),
        (eq, "$g_sod_lezalit_ief_discipline_result_grade", 2),
        (str_store_string, s1, "@The trial held because the drill was corrected before fear could become the only teacher."),
      (else_try),
        (eq, "$g_sod_lezalit_ief_discipline_result_grade", 1),
        (str_store_string, s1, "@The trial held quickly and coldly. The men obeyed, but nobody mistook silence for trust."),
      (else_try),
        (str_store_string, s1, "@The captured Imperial drill is still untested in front of the men who must carry it."),
      (try_end),
    ],
    [
      ("lezalit_discipline_reform", [
          (main_party_has_troop, "trp_npc14"),
          (eq, "$g_sod_lezalit_ief_discipline_pending", 1),
          (eq, "$g_sod_lezalit_ief_discipline_witnessed", 1),
          (eq, "$g_sod_lezalit_ief_discipline_confronted", 1),
        ], "Reform the Imperial drill without chains or terror.",
        [
          (assign, "$g_sod_lezalit_ief_discipline_pending", 0),
          (assign, "$g_sod_lezalit_ief_discipline_result_grade", 3),
          (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_metadata, "$g_sod_lezalit_ief_discipline_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_lezalit_ief_reform, 4),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc14", 1),
          (call_script, "script_sod_companion_lezalit_apply_discipline_payoff"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc14"),
          (display_message, "@Lezalit breaks the captured Imperial drill and rebuilds it without cruelty. Ymira and Bunduk both notice.", 0x99CCFF),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("lezalit_discipline_harsh", [
          (main_party_has_troop, "trp_npc14"),
          (eq, "$g_sod_lezalit_ief_discipline_pending", 1),
          (eq, "$g_sod_lezalit_ief_discipline_witnessed", 1),
          (eq, "$g_sod_lezalit_ief_discipline_confronted", 1),
        ], "Use fear. The line must obey before it understands.",
        [
          (assign, "$g_sod_lezalit_ief_discipline_pending", 0),
          (assign, "$g_sod_lezalit_ief_discipline_result_grade", 1),
          (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_metadata, "$g_sod_lezalit_ief_discipline_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_lezalit_ief_harsh, 4),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc14", 0),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc14"),
          (troop_set_slot, "trp_npc14", slot_troop_companion_warning_state, sod_companion_warning_acknowledged),
          (display_message, "@Lezalit turns victory over the Imperials into a hard discipline order. The lesson holds, but it chills the company.", 0xCCAA66),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("lezalit_discipline_refuse", [
          (main_party_has_troop, "trp_npc14"),
          (eq, "$g_sod_lezalit_ief_discipline_pending", 1),
          (eq, "$g_sod_lezalit_ief_discipline_witnessed", 1),
          (eq, "$g_sod_lezalit_ief_discipline_confronted", 1),
        ], "Refuse the lesson. The Imperial method is poison.",
        [
          (assign, "$g_sod_lezalit_ief_discipline_pending", 0),
          (assign, "$g_sod_lezalit_ief_discipline_result_grade", 0),
          (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_metadata, "$g_sod_lezalit_ief_discipline_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc14", -6),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc14"),
          (troop_set_slot, "trp_npc14", slot_troop_companion_warning_state, sod_companion_warning_pending),
          (display_message, "@Lezalit closes the captured manuals without comment. His warning waits behind the silence.", 0xCC6666),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("lezalit_discipline_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("lezalit_drill_trial", mnf_scale_picture|mnf_enable_hot_keys,
   "Lezalit forms the line at the edge of camp with the captured Imperial notes folded in one gloved hand. The ranker who spoke against the lash stands where the old manual would mark him for punishment.^^A scout calls contact from the dark scrub. Lezalit does not smile. 'Good. A doctrine that cannot survive interruption is only theater.'",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("lezalit_trial_explain", [
          (main_party_has_troop, "trp_npc14"),
          (eq, "$g_sod_lezalit_ief_discipline_pending", 1),
          (eq, "$g_sod_lezalit_ief_discipline_witnessed", 1),
          (eq, "$g_sod_lezalit_ief_discipline_confronted", 0),
        ], "Stand the line and make Lezalit explain every hard order.",
        [
          (modify_visitors_at_site, "scn_random_scene"),
          (reset_visitors),
          (set_visitor, 0, "trp_player"),
          (set_visitor, 1, "trp_npc14"),
          (set_visitor, 2, "trp_watchman"),
          (set_visitor, 3, "trp_caravan_guard"),
          (set_visitor, 10, "trp_bandit"),
          (set_visitor, 11, "trp_brigand"),
          (set_visitor, 12, "trp_henchman"),
          (set_jump_mission, "mt_companion_lezalit_drill_trial"),
          (jump_to_scene, "scn_random_scene"),
          (change_screen_mission),
        ]
      ),
      ("lezalit_trial_correct", [
          (main_party_has_troop, "trp_npc14"),
          (eq, "$g_sod_lezalit_ief_discipline_pending", 1),
          (eq, "$g_sod_lezalit_ief_discipline_witnessed", 1),
          (eq, "$g_sod_lezalit_ief_discipline_confronted", 0),
        ], "Cut the punishments, keep the drill, and run it again before contact lands.",
        [
          (assign, "$g_sod_lezalit_ief_discipline_confronted", 1),
          (assign, "$g_sod_lezalit_ief_discipline_result_grade", 2),
          (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_metadata, "$g_sod_lezalit_ief_discipline_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_train_troops, 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc14"),
          (display_message, "@The line moves faster when the useless punishments are cut away. Lezalit dislikes the proof mostly because it is proof.", 0xCCCC66),
          (start_map_conversation, "trp_npc14"),
        ]
      ),
      ("lezalit_trial_mark", [
          (main_party_has_troop, "trp_npc14"),
          (eq, "$g_sod_lezalit_ief_discipline_pending", 1),
          (eq, "$g_sod_lezalit_ief_discipline_witnessed", 1),
          (eq, "$g_sod_lezalit_ief_discipline_confronted", 0),
        ], "Mark the slowest man. The lesson must bite before the enemy does.",
        [
          (assign, "$g_sod_lezalit_ief_discipline_confronted", 1),
          (assign, "$g_sod_lezalit_ief_discipline_result_grade", 1),
          (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_metadata, "$g_sod_lezalit_ief_discipline_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_lezalit_ief_harsh, 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc14"),
          (display_message, "@The line moves cleanly and looks at the marked man instead of the enemy. Lezalit records the result. Bunduk records the cost.", 0xCC9966),
          (start_map_conversation, "trp_npc14"),
        ]
      ),
      ("lezalit_trial_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("lezalit_drill_trial_succeeded", mnf_scale_picture|mnf_enable_hot_keys,
   "The line wheels, locks, and answers the attack without becoming a mob. Lezalit lowers the captured manual like a man discovering that evidence has insulted him personally.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_lezalit_ief_discipline_confronted", 1),
      (try_begin),
        (le, "$g_sod_lezalit_ief_discipline_result_grade", 0),
        (assign, "$g_sod_lezalit_ief_discipline_result_grade", 3),
      (try_end),
      (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_metadata, "$g_sod_lezalit_ief_discipline_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc14"),
    ],
    [
      ("lezalit_trial_after", [], "Settle doctrine with Lezalit.",
        [
          (start_map_conversation, "trp_npc14"),
        ]
      ),
    ]
  ),

("lezalit_drill_trial_failed", mnf_scale_picture|mnf_enable_hot_keys,
   "The line survives, but not cleanly. Some men move too late. Some look over their shoulders for punishment before they look at the enemy. Lezalit says nothing until the wounded are counted.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_lezalit_ief_discipline_confronted", 1),
      (assign, "$g_sod_lezalit_ief_discipline_result_grade", -1),
      (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_lezalit_discipline_without_chains", slot_quest_sod_runtime_metadata, "$g_sod_lezalit_ief_discipline_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc14"),
    ],
    [
      ("lezalit_trial_failed_after", [], "Face Lezalit's report.",
        [
          (start_map_conversation, "trp_npc14"),
        ]
      ),
    ]
  ),
]
