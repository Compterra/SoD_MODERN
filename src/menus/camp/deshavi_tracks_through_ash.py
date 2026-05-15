MENUS = [
("deshavi_tracks_through_ash", mnf_scale_picture|mnf_enable_hot_keys,
   "Deshavi kneels beside a trail most of the company would have trampled flat. Broken grass, ash, a scrap of rope, and the wrong kind of silence tell her enough.^^{reg1?The signs point to hungry people moving badly and hiding worse.:The signs point to freed captives, with Slaver hunters close enough to smell fear.} Deshavi has followed the trail, faced what waited at its end, and now watches what lesson you take from it.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (try_begin),
        (this_or_next|neg|main_party_has_troop, "trp_npc7"),
        (neq, "$g_sod_deshavi_trail_warning_pending", 1),
        (assign, "$g_sod_deshavi_trail_warning_pending", 0),
        (assign, "$g_sod_deshavi_trail_warning_cause", 0),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (eq, "$g_sod_deshavi_trail_warning_cause", 2),
        (assign, reg1, 1),
      (else_try),
        (assign, reg1, 0),
      (try_end),
    ],
    [
      ("deshavi_tracks_shelter", [
          (main_party_has_troop, "trp_npc7"),
          (eq, "$g_sod_deshavi_trail_warning_pending", 1),
          (eq, "$g_sod_deshavi_trail_witnessed", 1),
          (eq, "$g_sod_deshavi_trail_confronted", 1),
        ], "Follow the trail, shelter the vulnerable, and cover their tracks.",
        [
          (assign, "$g_sod_deshavi_trail_warning_pending", 0),
          (assign, "$g_sod_deshavi_trail_result_grade", 3),
          (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_metadata, "$g_sod_deshavi_trail_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_scout_warning, 3),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_food_security, 2),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc7", 1),
          (call_script, "script_sod_companion_deshavi_apply_trail_payoff"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc7"),
          (display_message, "@Deshavi hides the weak, fouls the pursuit, and leaves the hunters chasing old ash. Tracks Through Ash remembers shelter.", 0x99CCFF),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("deshavi_tracks_ambush", [
          (main_party_has_troop, "trp_npc7"),
          (eq, "$g_sod_deshavi_trail_warning_pending", 1),
          (eq, "$g_sod_deshavi_trail_witnessed", 1),
          (eq, "$g_sod_deshavi_trail_confronted", 1),
        ], "Use the trail to set an ambush before helping survivors move.",
        [
          (assign, "$g_sod_deshavi_trail_warning_pending", 0),
          (try_begin),
            (le, "$g_sod_deshavi_trail_result_grade", 0),
            (assign, "$g_sod_deshavi_trail_result_grade", 2),
          (try_end),
          (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_metadata, "$g_sod_deshavi_trail_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_safe_roadcraft, 2),
          (call_script, "script_sod_companion_shift_approval", "trp_npc7", 2),
          (try_begin),
            (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
            (troop_set_slot, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (else_try),
            (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
            (call_script, "script_sod_companion_advance_personal_quest", "trp_npc7", 1),
            (call_script, "script_sod_companion_deshavi_apply_trail_payoff"),
          (try_end),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc7"),
          (display_message, "@The ambush breaks the pursuit, and Deshavi makes sure the survivors are not left as bait.", 0xCCCC66),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("deshavi_tracks_hunt_only", [
          (main_party_has_troop, "trp_npc7"),
          (eq, "$g_sod_deshavi_trail_warning_pending", 1),
          (eq, "$g_sod_deshavi_trail_witnessed", 1),
          (eq, "$g_sod_deshavi_trail_confronted", 1),
        ], "Hunt the pursuers. The weak must keep moving on their own.",
        [
          (assign, "$g_sod_deshavi_trail_warning_pending", 0),
          (assign, "$g_sod_deshavi_trail_result_grade", 1),
          (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_metadata, "$g_sod_deshavi_trail_result_grade"),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc7", 0),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc7"),
          (troop_set_slot, "trp_npc7", slot_troop_companion_warning_state, sod_companion_warning_pending),
          (display_message, "@The hunters bleed, but Deshavi keeps looking back at the tracks you chose not to follow.", 0xCC6666),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("deshavi_tracks_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("deshavi_tracks_trail_climax", mnf_scale_picture|mnf_enable_hot_keys,
   "Beyond the village, Deshavi finds the signs the witness could not name: heel marks where captives were pulled upright, ash rubbed into boot soles, and a watching place cut into the brush.^^The trail has not gone cold. It has gone quiet because someone is waiting for you to hurry.",
   "none",
    [
      (set_background_mesh, "mesh_pic_bandits"),
    ],
    [
      ("deshavi_trail_rescue", [
          (main_party_has_troop, "trp_npc7"),
          (eq, "$g_sod_deshavi_trail_warning_pending", 1),
          (eq, "$g_sod_deshavi_trail_witnessed", 1),
          (eq, "$g_sod_deshavi_trail_confronted", 0),
        ], "Move with Deshavi and break the captive camp.",
        [
          (party_get_slot, ":scene_to_use", "$current_town", slot_castle_exterior),
          (modify_visitors_at_site, ":scene_to_use"),
          (reset_visitors),
          (set_visitor, 0, "trp_player"),
          (set_visitor, 1, "trp_npc7"),
          (set_visitor, 2, "trp_farmer"),
          (set_visitor, 3, "trp_slave_female"),
          (try_begin),
            (eq, "$g_sod_deshavi_trail_warning_cause", 2),
            (set_visitor, 10, "trp_slave_driver"),
          (else_try),
            (set_visitor, 10, "trp_bandit"),
          (try_end),
          (set_visitor, 11, "trp_brigand"),
          (set_visitor, 12, "trp_henchman"),
          (set_visitor, 13, "trp_bandit"),
          (set_jump_mission, "mt_companion_deshavi_trail_rescue"),
          (jump_to_scene, ":scene_to_use"),
          (change_screen_mission),
        ]
      ),
      ("deshavi_trail_reverse_ambush", [
          (main_party_has_troop, "trp_npc7"),
          (eq, "$g_sod_deshavi_trail_warning_pending", 1),
          (eq, "$g_sod_deshavi_trail_witnessed", 1),
          (eq, "$g_sod_deshavi_trail_confronted", 0),
        ], "Let Deshavi lay false tracks, then spring the ambush on your terms.",
        [
          (assign, "$g_sod_deshavi_trail_confronted", 1),
          (assign, "$g_sod_deshavi_trail_result_grade", 2),
          (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_metadata, "$g_sod_deshavi_trail_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_safe_roadcraft, 2),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc7"),
          (display_message, "@Deshavi turns the pursuers' own impatience against them. Some captives scatter, but the chase breaks.", 0xCCCC66),
          (start_map_conversation, "trp_npc7"),
        ]
      ),
      ("deshavi_trail_hunt_first", [
          (main_party_has_troop, "trp_npc7"),
          (eq, "$g_sod_deshavi_trail_warning_pending", 1),
          (eq, "$g_sod_deshavi_trail_witnessed", 1),
          (eq, "$g_sod_deshavi_trail_confronted", 0),
        ], "Strike the pursuers first. Survivors can move while the hunters bleed.",
        [
          (assign, "$g_sod_deshavi_trail_confronted", 1),
          (assign, "$g_sod_deshavi_trail_result_grade", 1),
          (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_metadata, "$g_sod_deshavi_trail_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc7", -2),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc7"),
          (display_message, "@The pursuers die quickly. Deshavi marks every track left by people who had to save themselves.", 0xCC9966),
          (start_map_conversation, "trp_npc7"),
        ]
      ),
      ("deshavi_trail_leave", [], "Leave the trail for now.",
        [
          (jump_to_menu, "mnu_village"),
        ]
      ),
    ]
  ),

("deshavi_tracks_rescue_succeeded", mnf_scale_picture|mnf_enable_hot_keys,
   "The hidden camp breaks. Deshavi moves through the smoke with a knife low and her eyes on the captives, not the bodies. Some run. Some need lifting. For once, the trail away from ash has enough guards.",
   "none",
    [
      (set_background_mesh, "mesh_pic_bandits"),
      (assign, "$g_sod_deshavi_trail_confronted", 1),
      (try_begin),
        (le, "$g_sod_deshavi_trail_result_grade", 0),
        (assign, "$g_sod_deshavi_trail_result_grade", 3),
      (try_end),
      (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_metadata, "$g_sod_deshavi_trail_result_grade"),
      (call_script, "script_sod_companion_apply_player_action", sod_companion_action_scout_warning, 3),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc7"),
    ],
    [
      ("deshavi_rescue_aftermath", [], "Speak with Deshavi about the trail.",
        [
          (start_map_conversation, "trp_npc7"),
        ]
      ),
    ]
  ),

("deshavi_tracks_rescue_failed", mnf_scale_picture|mnf_enable_hot_keys,
   "The trail becomes shouting, then smoke. Deshavi drags you clear when the fight turns, but her face stays on the tracks that keep going without you. The quest is not lost, yet the next answer will carry this failure.",
   "none",
    [
      (set_background_mesh, "mesh_pic_bandits"),
      (assign, "$g_sod_deshavi_trail_confronted", 1),
      (assign, "$g_sod_deshavi_trail_result_grade", -1),
      (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_metadata, "$g_sod_deshavi_trail_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc7"),
    ],
    [
      ("deshavi_rescue_failed_aftermath", [], "Face Deshavi's judgment.",
        [
          (start_map_conversation, "trp_npc7"),
        ]
      ),
    ]
  ),
]
