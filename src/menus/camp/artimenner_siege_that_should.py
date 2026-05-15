MENUS = [
("artimenner_siege_that_should", mnf_scale_picture|mnf_enable_hot_keys,
   "Artimenner has laid the siege design across a plank, weighted by stones, tools, and one splintered brace he clearly despises. {s1}^^The weak point has been witnessed and the repair watch has been survived. Now he is asking whether the army wants the works to hold, or merely wants someone convenient to blame when timber obeys weight instead of pride.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (try_begin),
        (this_or_next|neg|main_party_has_troop, "trp_npc15"),
        (neq, "$g_sod_artimenner_siege_pending", 1),
        (assign, "$g_sod_artimenner_siege_pending", 0),
        (assign, "$g_sod_artimenner_siege_cause", 0),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (eq, "$g_sod_artimenner_siege_result_grade", -1),
        (str_store_string, s1, "@The repair watch held badly; the weak point is corrected, but only after bruises, broken tools, and a silence Artimenner finds mathematically damning."),
      (else_try),
        (eq, "$g_sod_artimenner_siege_result_grade", 3),
        (str_store_string, s1, "@The repair watch held because men guarded the work instead of arguing with it."),
      (else_try),
        (eq, "$g_sod_artimenner_siege_result_grade", 2),
        (str_store_string, s1, "@The repair watch held because the design was simplified before sabotage and haste could share the same mask."),
      (else_try),
        (eq, "$g_sod_artimenner_siege_result_grade", 1),
        (str_store_string, s1, "@The repair watch held because the workers took the blame before the plan did. Artimenner has not mistaken that for engineering."),
      (else_try),
        (eq, "$g_sod_artimenner_siege_cause", 2),
        (str_store_string, s1, "@The tower will stand only if the design is rebuilt around the load."),
      (else_try),
        (str_store_string, s1, "@The ladders will carry men only if the rushed joints are corrected."),
      (try_end),
    ],
    [
      ("artimenner_siege_rebuild", [
          (main_party_has_troop, "trp_npc15"),
          (eq, "$g_sod_artimenner_siege_pending", 1),
          (eq, "$g_sod_artimenner_siege_witnessed", 1),
          (eq, "$g_sod_artimenner_siege_confronted", 1),
        ], "Give Artimenner time and materials to rebuild the works properly.",
        [
          (assign, "$g_sod_artimenner_siege_pending", 0),
          (assign, "$g_sod_artimenner_siege_result_grade", 3),
          (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_metadata, "$g_sod_artimenner_siege_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_siege_preparation, 3),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc15", 1),
          (call_script, "script_sod_companion_artimenner_apply_siege_payoff"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc15"),
          (display_message, "@The works hold because they were built to hold. The Siege That Should Have Worked remembers respected design.", 0x99CCFF),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("artimenner_siege_improvise", [
          (main_party_has_troop, "trp_npc15"),
          (eq, "$g_sod_artimenner_siege_pending", 1),
          (eq, "$g_sod_artimenner_siege_witnessed", 1),
          (eq, "$g_sod_artimenner_siege_confronted", 1),
        ], "Ask him to improvise a leaner plan with what the army has.",
        [
          (assign, "$g_sod_artimenner_siege_pending", 0),
          (try_begin),
            (lt, "$g_sod_artimenner_siege_result_grade", 2),
            (assign, "$g_sod_artimenner_siege_result_grade", 2),
          (try_end),
          (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_metadata, "$g_sod_artimenner_siege_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc15", 2),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc15", 1),
          (call_script, "script_sod_companion_artimenner_apply_siege_payoff"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc15"),
          (display_message, "@Artimenner accepts the inferior plan because it is still a plan, not glorious nonsense.", 0xCCCC66),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("artimenner_siege_blame", [
          (main_party_has_troop, "trp_npc15"),
          (eq, "$g_sod_artimenner_siege_pending", 1),
          (eq, "$g_sod_artimenner_siege_witnessed", 1),
          (eq, "$g_sod_artimenner_siege_confronted", 1),
        ], "Tell Artimenner he will be blamed if the works fail.",
        [
          (assign, "$g_sod_artimenner_siege_pending", 0),
          (assign, "$g_sod_artimenner_siege_result_grade", 1),
          (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_metadata, "$g_sod_artimenner_siege_result_grade"),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc15", 0),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc15"),
          (troop_set_slot, "trp_npc15", slot_troop_companion_warning_state, sod_companion_warning_pending),
          (display_message, "@Artimenner's voice goes flat. A neat report cannot carry a ladder.", 0xCC6666),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("artimenner_siege_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("artimenner_repair_watch", mnf_scale_picture|mnf_enable_hot_keys,
   "Artimenner sets chalk marks on the bad joints and braces, then points workers into place as if arranging a proof. The hurry around the siege works has attracted exactly the wrong kind of help: men trying to save time by cutting corners, and saboteurs trying to make the corner cut look like an accident.^^'Guard the work,' he says. 'Not me. The work.'",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("artimenner_watch_guard", [
          (main_party_has_troop, "trp_npc15"),
          (eq, "$g_sod_artimenner_siege_pending", 1),
          (eq, "$g_sod_artimenner_siege_witnessed", 1),
          (eq, "$g_sod_artimenner_siege_confronted", 0),
        ], "Guard the repair crew while Artimenner corrects the design.",
        [
          (modify_visitors_at_site, "scn_random_scene"),
          (reset_visitors),
          (set_visitor, 0, "trp_player"),
          (set_visitor, 1, "trp_npc15"),
          (set_visitor, 2, "trp_watchman"),
          (set_visitor, 3, "trp_caravan_guard"),
          (set_visitor, 10, "trp_bandit"),
          (set_visitor, 11, "trp_brigand"),
          (set_visitor, 12, "trp_henchman"),
          (set_jump_mission, "mt_companion_artimenner_repair_watch"),
          (jump_to_scene, "scn_random_scene"),
          (change_screen_mission),
        ]
      ),
      ("artimenner_watch_simplify", [
          (main_party_has_troop, "trp_npc15"),
          (eq, "$g_sod_artimenner_siege_pending", 1),
          (eq, "$g_sod_artimenner_siege_witnessed", 1),
          (eq, "$g_sod_artimenner_siege_confronted", 0),
        ], "Simplify the design now and keep the workers close enough to supervise.",
        [
          (assign, "$g_sod_artimenner_siege_confronted", 1),
          (assign, "$g_sod_artimenner_siege_result_grade", 2),
          (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_metadata, "$g_sod_artimenner_siege_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_siege_preparation, 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc15"),
          (display_message, "@The works become less elegant and more honest. Artimenner calls that an improvement over beautiful collapse.", 0xCCCC66),
          (start_map_conversation, "trp_npc15"),
        ]
      ),
      ("artimenner_watch_blame_workers", [
          (main_party_has_troop, "trp_npc15"),
          (eq, "$g_sod_artimenner_siege_pending", 1),
          (eq, "$g_sod_artimenner_siege_witnessed", 1),
          (eq, "$g_sod_artimenner_siege_confronted", 0),
        ], "Put the workers under threat. Fear will keep the measurements exact.",
        [
          (assign, "$g_sod_artimenner_siege_confronted", 1),
          (assign, "$g_sod_artimenner_siege_result_grade", 1),
          (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_metadata, "$g_sod_artimenner_siege_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc15", -2),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc15"),
          (display_message, "@The workers measure twice because they fear what happens if they do not. Artimenner measures the cost and says nothing flattering.", 0xCC9966),
          (start_map_conversation, "trp_npc15"),
        ]
      ),
      ("artimenner_watch_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("artimenner_repair_watch_succeeded", mnf_scale_picture|mnf_enable_hot_keys,
   "The saboteurs break against guards and corrected timber. Artimenner checks the repaired joint before he checks whether anyone is impressed, which means he has not lost his priorities.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_artimenner_siege_confronted", 1),
      (try_begin),
        (le, "$g_sod_artimenner_siege_result_grade", 0),
        (assign, "$g_sod_artimenner_siege_result_grade", 3),
      (try_end),
      (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_metadata, "$g_sod_artimenner_siege_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc15"),
    ],
    [
      ("artimenner_watch_after", [], "Settle the siege design with Artimenner.",
        [
          (start_map_conversation, "trp_npc15"),
        ]
      ),
    ]
  ),

("artimenner_repair_watch_failed", mnf_scale_picture|mnf_enable_hot_keys,
   "The repair watch holds after too much scrambling and too many shouted measurements. The works can still be corrected, but Artimenner looks at the wasted tools like they are witnesses for the prosecution.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_artimenner_siege_confronted", 1),
      (assign, "$g_sod_artimenner_siege_result_grade", -1),
      (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_metadata, "$g_sod_artimenner_siege_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc15"),
    ],
    [
      ("artimenner_watch_failed_after", [], "Face Artimenner's report.",
        [
          (start_map_conversation, "trp_npc15"),
        ]
      ),
    ]
  ),
]
