MENUS = [
("rolf_name_worth_wearing", mnf_scale_picture|mnf_enable_hot_keys,
   "The tournament crowd is gone, but its echoes have followed the company back to camp. {s1}^^A town witness has weighed Rolf's name, and the public proof has shown whether his claim can do work while people are watching.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (try_begin),
        (this_or_next|neg|main_party_has_troop, "trp_npc4"),
        (neq, "$g_sod_rolf_name_challenge_pending", 1),
        (assign, "$g_sod_rolf_name_challenge_pending", 0),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (eq, "$g_sod_rolf_name_challenge_result_grade", -1),
        (str_store_string, s1, "@The proof went poorly enough that even Rolf has stopped calling the bruises decorative."),
      (else_try),
        (eq, "$g_sod_rolf_name_challenge_result_grade", 3),
        (str_store_string, s1, "@The proof made the name useful in front of witnesses."),
      (else_try),
        (eq, "$g_sod_rolf_name_challenge_result_grade", 2),
        (str_store_string, s1, "@The proof preserved dignity and asked the name to earn its applause later."),
      (else_try),
        (eq, "$g_sod_rolf_name_challenge_result_grade", 1),
        (str_store_string, s1, "@The proof protected the performance more than the people watching it."),
      (else_try),
        (str_store_string, s1, "@Some cheered Rolf's noble bearing. Some repeated the old question with wine on their breath: noble of where, exactly?"),
      (try_end),
    ],
    [
      ("rolf_name_earn", [
          (main_party_has_troop, "trp_npc4"),
          (eq, "$g_sod_rolf_name_challenge_pending", 1),
          (eq, "$g_sod_rolf_name_challenge_witnessed", 1),
          (eq, "$g_sod_rolf_name_challenge_confronted", 1),
        ], "Have Rolf answer with service, not embellishment.",
        [
          (assign, "$g_sod_rolf_name_challenge_pending", 0),
          (assign, "$g_sod_rolf_name_challenge_result_grade", 3),
          (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_metadata, "$g_sod_rolf_name_challenge_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_tournament_glory, 2),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc4", 1),
          (call_script, "script_sod_companion_rolf_apply_name_payoff"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc4"),
          (display_message, "@Rolf lets the crowd have a smaller story and the company a better man. A Name Worth Wearing remembers earned dignity.", 0x99CCFF),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("rolf_name_defend", [
          (main_party_has_troop, "trp_npc4"),
          (eq, "$g_sod_rolf_name_challenge_pending", 1),
          (eq, "$g_sod_rolf_name_challenge_witnessed", 1),
          (eq, "$g_sod_rolf_name_challenge_confronted", 1),
        ], "Defend Rolf's dignity without asking him to prove the tale.",
        [
          (assign, "$g_sod_rolf_name_challenge_pending", 0),
          (try_begin),
            (lt, "$g_sod_rolf_name_challenge_result_grade", 2),
            (assign, "$g_sod_rolf_name_challenge_result_grade", 2),
          (try_end),
          (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_metadata, "$g_sod_rolf_name_challenge_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc4", 3),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc4", 1),
          (call_script, "script_sod_companion_rolf_apply_name_payoff"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc4"),
          (display_message, "@Rolf's bow is magnificent. The claim survives, but now it owes the company conduct worthy of it.", 0xCCCC66),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("rolf_name_expose", [
          (main_party_has_troop, "trp_npc4"),
          (eq, "$g_sod_rolf_name_challenge_pending", 1),
          (eq, "$g_sod_rolf_name_challenge_witnessed", 1),
          (eq, "$g_sod_rolf_name_challenge_confronted", 1),
        ], "Strip away the performance in front of the company.",
        [
          (assign, "$g_sod_rolf_name_challenge_pending", 0),
          (assign, "$g_sod_rolf_name_challenge_result_grade", 1),
          (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_metadata, "$g_sod_rolf_name_challenge_result_grade"),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc4", 0),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc4"),
          (troop_set_slot, "trp_npc4", slot_troop_companion_warning_state, sod_companion_warning_pending),
          (display_message, "@The story breaks loudly. Rolf keeps his posture, but every polished word costs him more.", 0xCC6666),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("rolf_name_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("rolf_public_proof", mnf_scale_picture|mnf_enable_hot_keys,
   "The town witness was right: a name remembered only in tavern warmth cools fast. Rolf finds the little crowd still willing to watch him, and that is almost worse than mockery. Then trouble arrives where everyone can see it.^^Rolf adjusts his cloak. 'If they insist on a public answer, let it at least have composition.'",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("rolf_proof_service", [
          (main_party_has_troop, "trp_npc4"),
          (eq, "$g_sod_rolf_name_challenge_pending", 1),
          (eq, "$g_sod_rolf_name_challenge_witnessed", 1),
          (eq, "$g_sod_rolf_name_challenge_confronted", 0),
        ], "Let Rolf prove the name by defending people in sight of the crowd.",
        [
          (modify_visitors_at_site, "scn_random_scene"),
          (reset_visitors),
          (set_visitor, 0, "trp_player"),
          (set_visitor, 1, "trp_npc4"),
          (set_visitor, 2, "trp_watchman"),
          (set_visitor, 3, "trp_farmer"),
          (set_visitor, 10, "trp_bandit"),
          (set_visitor, 11, "trp_brigand"),
          (set_visitor, 12, "trp_henchman"),
          (set_jump_mission, "mt_companion_rolf_public_proof"),
          (jump_to_scene, "scn_random_scene"),
          (change_screen_mission),
        ]
      ),
      ("rolf_proof_patron", [
          (main_party_has_troop, "trp_npc4"),
          (eq, "$g_sod_rolf_name_challenge_pending", 1),
          (eq, "$g_sod_rolf_name_challenge_witnessed", 1),
          (eq, "$g_sod_rolf_name_challenge_confronted", 0),
          (store_troop_gold, ":gold", "trp_player"),
          (ge, ":gold", 200),
        ], "Have Rolf sponsor public repairs and make the name useful.",
        [
          (assign, "$g_sod_rolf_name_challenge_confronted", 1),
          (assign, "$g_sod_rolf_name_challenge_result_grade", 2),
          (call_script, "script_sod_player_charge_gold", 200),
          (eq, reg1, 1),
          (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_metadata, "$g_sod_rolf_name_challenge_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_tournament_glory, 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc4"),
          (display_message, "@Rolf's name buys repairs in public. He calls it patronage. The town calls it useful.", 0xCCCC66),
          (start_map_conversation, "trp_npc4"),
        ]
      ),
      ("rolf_proof_theater", [
          (main_party_has_troop, "trp_npc4"),
          (eq, "$g_sod_rolf_name_challenge_pending", 1),
          (eq, "$g_sod_rolf_name_challenge_witnessed", 1),
          (eq, "$g_sod_rolf_name_challenge_confronted", 0),
        ], "Stage a grand answer and silence the mockery with performance.",
        [
          (assign, "$g_sod_rolf_name_challenge_confronted", 1),
          (assign, "$g_sod_rolf_name_challenge_result_grade", 1),
          (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_metadata, "$g_sod_rolf_name_challenge_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc4", -2),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc4"),
          (display_message, "@The crowd enjoys the answer. Rolf enjoys it too much. The name survives, and remains hungry.", 0xCC9966),
          (start_map_conversation, "trp_npc4"),
        ]
      ),
      ("rolf_proof_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("rolf_public_proof_succeeded", mnf_scale_picture|mnf_enable_hot_keys,
   "The trouble breaks, and Rolf remains standing where witnesses can see him. He gives the crowd a bow so deep it nearly becomes honest.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_rolf_name_challenge_confronted", 1),
      (try_begin),
        (le, "$g_sod_rolf_name_challenge_result_grade", 0),
        (assign, "$g_sod_rolf_name_challenge_result_grade", 3),
      (try_end),
      (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_metadata, "$g_sod_rolf_name_challenge_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc4"),
    ],
    [
      ("rolf_public_proof_after", [], "Settle the name with Rolf.",
        [
          (start_map_conversation, "trp_npc4"),
        ]
      ),
    ]
  ),

("rolf_public_proof_failed", mnf_scale_picture|mnf_enable_hot_keys,
   "The crowd sees more panic than polish. Rolf survives the public proof, but the name limps away with him.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_rolf_name_challenge_confronted", 1),
      (assign, "$g_sod_rolf_name_challenge_result_grade", -1),
      (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_metadata, "$g_sod_rolf_name_challenge_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc4"),
    ],
    [
      ("rolf_public_proof_failed_after", [], "Face Rolf's public answer.",
        [
          (start_map_conversation, "trp_npc4"),
        ]
      ),
    ]
  ),
]
