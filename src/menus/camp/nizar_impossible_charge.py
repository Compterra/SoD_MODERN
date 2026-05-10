MENUS = [
("nizar_impossible_charge", mnf_scale_picture|mnf_enable_hot_keys,
   "Nizar sketches a charge route in the dust with the bright confidence of a man who trusts both horses and applause. The plan is beautiful, dangerous, and almost certainly improved by the fact that nobody has tried it yet.^^He looks up smiling. There is a charge men call impossible because they lack imagination. There is also the other kind.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (try_begin),
        (this_or_next|neg|main_party_has_troop, "trp_npc13"),
        (neq, "$g_sod_nizar_charge_pending", 1),
        (assign, "$g_sod_nizar_charge_pending", 0),
        (assign, "$g_sod_nizar_charge_witnessed", 0),
        (assign, "$g_sod_nizar_charge_confronted", 0),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (this_or_next|neq, "$g_sod_nizar_charge_witnessed", 1),
        (neq, "$g_sod_nizar_charge_confronted", 1),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
    ],
    [
      ("nizar_charge_responsible", [
          (main_party_has_troop, "trp_npc13"),
          (eq, "$g_sod_nizar_charge_pending", 1),
          (eq, "$g_sod_nizar_charge_witnessed", 1),
          (eq, "$g_sod_nizar_charge_confronted", 1),
        ], "Make the charge work by planning the way out first.",
        [
          (assign, "$g_sod_nizar_charge_pending", 0),
          (assign, "$g_sod_nizar_charge_result_grade", 3),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_tournament_glory, 2),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc13", 1),
          (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_metadata, "$g_sod_nizar_charge_result_grade"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc13"),
          (call_script, "script_sod_companion_nizar_apply_charge_payoff"),
          (display_message, "@The charge keeps its drama and gains an exit. The Impossible Charge remembers glory with survivors.", 0x99CCFF),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("nizar_charge_daring", [
          (main_party_has_troop, "trp_npc13"),
          (eq, "$g_sod_nizar_charge_pending", 1),
          (eq, "$g_sod_nizar_charge_witnessed", 1),
          (eq, "$g_sod_nizar_charge_confronted", 1),
        ], "Take the dazzling charge before anyone can make it sensible.",
        [
          (assign, "$g_sod_nizar_charge_pending", 0),
          (try_begin),
            (lt, "$g_sod_nizar_charge_result_grade", 2),
            (assign, "$g_sod_nizar_charge_result_grade", 2),
          (try_end),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_hard_victory, 2),
          (call_script, "script_sod_companion_shift_approval", "trp_npc13", 2),
          (try_begin),
            (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
            (troop_set_slot, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (else_try),
            (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
            (call_script, "script_sod_companion_advance_personal_quest", "trp_npc13", 1),
            (call_script, "script_sod_companion_nizar_apply_charge_payoff"),
          (try_end),
          (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_metadata, "$g_sod_nizar_charge_result_grade"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc13"),
          (display_message, "@Nizar laughs like a banner in high wind. The charge will need luck, speed, and a better ending than most songs earn.", 0xCCCC66),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("nizar_charge_blood_legend", [
          (main_party_has_troop, "trp_npc13"),
          (eq, "$g_sod_nizar_charge_pending", 1),
          (eq, "$g_sod_nizar_charge_witnessed", 1),
          (eq, "$g_sod_nizar_charge_confronted", 1),
        ], "Spend blood for a legend no one can ignore.",
        [
          (assign, "$g_sod_nizar_charge_pending", 0),
          (assign, "$g_sod_nizar_charge_result_grade", 1),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc13", 0),
          (troop_set_slot, "trp_npc13", slot_troop_companion_warning_state, sod_companion_warning_pending),
          (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_metadata, "$g_sod_nizar_charge_result_grade"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc13"),
          (display_message, "@The story will travel farther than the burial count. Nizar smiles late, as if hearing the cost arrive after the applause.", 0xCC6666),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("nizar_charge_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("nizar_charge_lane_test", mnf_scale_picture|mnf_enable_hot_keys,
   "Nizar's dust map becomes ground underfoot: a blind turn, a ragged screen of scrub, and a gap that looks heroic only from far away. He grins as if danger has arrived wearing perfume.^^'There. We either make the impossible charge into a road, or we make it into a poem with too many dead men in the meter.'",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("nizar_lane_exit_first", [
          (main_party_has_troop, "trp_npc13"),
          (eq, "$g_sod_nizar_charge_pending", 1),
          (eq, "$g_sod_nizar_charge_witnessed", 1),
          (eq, "$g_sod_nizar_charge_confronted", 0),
        ], "Mark the exit first and make the charge earn its song.",
        [
          (assign, "$g_sod_nizar_charge_confronted", 1),
          (assign, "$g_sod_nizar_charge_result_grade", 3),
          (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_metadata, "$g_sod_nizar_charge_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc13", 3),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc13"),
          (display_message, "@Nizar makes a show of being offended by caution, then improves the route until even caution looks dramatic.", 0x99CCFF),
          (jump_to_menu, "mnu_nizar_impossible_charge"),
        ]
      ),
      ("nizar_lane_ride_it", [
          (main_party_has_troop, "trp_npc13"),
          (eq, "$g_sod_nizar_charge_pending", 1),
          (eq, "$g_sod_nizar_charge_witnessed", 1),
          (eq, "$g_sod_nizar_charge_confronted", 0),
        ], "Ride the charge lane with Nizar.",
        [
          (modify_visitors_at_site, "scn_random_scene"),
          (reset_visitors),
          (set_visitor, 0, "trp_player"),
          (set_visitor, 1, "trp_npc13"),
          (set_visitor, 2, "trp_mercenary_swordsman"),
          (set_visitor, 10, "trp_bandit"),
          (set_visitor, 11, "trp_brigand"),
          (set_visitor, 12, "trp_henchman"),
          (set_jump_mission, "mt_companion_nizar_charge_lane"),
          (jump_to_scene, "scn_random_scene"),
          (change_screen_mission),
        ]
      ),
      ("nizar_lane_applause_first", [
          (main_party_has_troop, "trp_npc13"),
          (eq, "$g_sod_nizar_charge_pending", 1),
          (eq, "$g_sod_nizar_charge_witnessed", 1),
          (eq, "$g_sod_nizar_charge_confronted", 0),
        ], "Make the charge louder, not safer.",
        [
          (assign, "$g_sod_nizar_charge_confronted", 1),
          (assign, "$g_sod_nizar_charge_result_grade", 1),
          (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_metadata, "$g_sod_nizar_charge_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc13", -3),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc13"),
          (display_message, "@The charge will be remembered. Nizar notices too late that remembering and surviving are different arts.", 0xCC9966),
          (jump_to_menu, "mnu_nizar_impossible_charge"),
        ]
      ),
      ("nizar_lane_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("nizar_charge_lane_succeeded", mnf_scale_picture|mnf_enable_hot_keys,
   "The charge hits, bends, and comes out the other side with breath still in it. Nizar laughs first, then checks who came with him before he laughs again.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_nizar_charge_confronted", 1),
      (try_begin),
        (le, "$g_sod_nizar_charge_result_grade", 0),
        (assign, "$g_sod_nizar_charge_result_grade", 2),
      (try_end),
      (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_metadata, "$g_sod_nizar_charge_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc13"),
    ],
    [
      ("nizar_charge_lane_after", [], "Settle the charge with Nizar.",
        [
          (jump_to_menu, "mnu_nizar_impossible_charge"),
        ]
      ),
    ]
  ),

("nizar_charge_lane_failed", mnf_scale_picture|mnf_enable_hot_keys,
   "The charge becomes a story before it becomes a victory. Nizar survives it, but the dust behind him is too quiet for applause.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_nizar_charge_confronted", 1),
      (assign, "$g_sod_nizar_charge_result_grade", -1),
      (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_metadata, "$g_sod_nizar_charge_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc13"),
    ],
    [
      ("nizar_charge_lane_failed_after", [], "Face Nizar after the broken charge.",
        [
          (jump_to_menu, "mnu_nizar_impossible_charge"),
        ]
      ),
    ]
  ),
]
