MENUS = [
("borcha_road_keeps_own", mnf_scale_picture|mnf_enable_hot_keys,
   "Borcha has the road drawn in dirt and boot cuts: {s3} at one end, {s4} at the other, and a side track too clean to trust.^^{reg1?The first plan smelled like profit, and Borcha has not forgotten who suggested bait.:The first plan was caution, and Borcha is watching whether caution becomes help.} The road has spoken through a witness and answered with steel. Now the lesson belongs to the company.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (try_begin),
        (this_or_next|neg|main_party_has_troop, "trp_npc1"),
        (neq, "$g_sod_borcha_road_pending", 1),
        (assign, "$g_sod_borcha_road_pending", 0),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (is_between, "$g_sod_borcha_road_origin_center", towns_begin, towns_end),
        (str_store_party_name_link, s3, "$g_sod_borcha_road_origin_center"),
      (else_try),
        (str_store_string, s3, "@the road town"),
      (try_end),
      (try_begin),
        (is_between, "$g_sod_borcha_road_destination_center", villages_begin, villages_end),
        (str_store_party_name_link, s4, "$g_sod_borcha_road_destination_center"),
      (else_try),
        (str_store_string, s4, "@the far village"),
      (try_end),
      (try_begin),
        (eq, "$g_sod_borcha_road_cause", 2),
        (assign, reg1, 1),
      (else_try),
        (assign, reg1, 0),
      (try_end),
    ],
    [
      ("borcha_road_safe", [
          (main_party_has_troop, "trp_npc1"),
          (eq, "$g_sod_borcha_road_witnessed", 1),
          (eq, "$g_sod_borcha_road_confronted", 1),
        ], "Mark the side road, warn travelers, and leave guards where the trap used to be.",
        [
          (assign, "$g_sod_borcha_road_pending", 0),
          (assign, "$g_sod_borcha_road_result_grade", 3),
          (quest_set_slot, "qst_companion_borcha_road_keeps_own", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_borcha_road_keeps_own", slot_quest_sod_runtime_metadata, "$g_sod_borcha_road_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_safe_roadcraft, 3),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc1", 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc1"),
          (display_message, "@The hidden route is marked, watched, and broken before it can swallow another caravan. Borcha says nothing grand. He only marks a safer road for the company.", 0x99CCFF),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("borcha_road_counter_ambush", [
          (main_party_has_troop, "trp_npc1"),
          (eq, "$g_sod_borcha_road_witnessed", 1),
          (eq, "$g_sod_borcha_road_confronted", 1),
        ], "Keep Borcha's counter-ambush standing until the road is clean.",
        [
          (assign, "$g_sod_borcha_road_pending", 0),
          (try_begin),
            (le, "$g_sod_borcha_road_result_grade", 0),
            (assign, "$g_sod_borcha_road_result_grade", 2),
          (try_end),
          (quest_set_slot, "qst_companion_borcha_road_keeps_own", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_borcha_road_keeps_own", slot_quest_sod_runtime_metadata, "$g_sod_borcha_road_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_safe_roadcraft, 2),
          (call_script, "script_sod_companion_shift_approval", "trp_npc1", 2),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc1", 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc1"),
          (display_message, "@Borcha keeps the ambush site baited until the raiders stop trusting their own road. It is useful, if not gentle.", 0xCCCC66),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("borcha_road_profit", [
          (main_party_has_troop, "trp_npc1"),
          (eq, "$g_sod_borcha_road_witnessed", 1),
          (eq, "$g_sod_borcha_road_confronted", 1),
        ], "Use the route for profit before anyone else learns it is safe.",
        [
          (assign, "$g_sod_borcha_road_pending", 0),
          (assign, "$g_sod_borcha_road_result_grade", 1),
          (quest_set_slot, "qst_companion_borcha_road_keeps_own", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_borcha_road_keeps_own", slot_quest_sod_runtime_metadata, "$g_sod_borcha_road_result_grade"),
          (call_script, "script_troop_add_gold", "trp_player", 250),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc1", 0),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc1"),
          (troop_set_slot, "trp_npc1", slot_troop_companion_warning_state, sod_companion_warning_pending),
          (display_message, "@The route yields coin and bad looks from Borcha. 'You can skin a road, sure. Then do not ask why it stops feeding you.'", 0xCC9966),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("borcha_road_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("borcha_road_counter_ambush", mnf_scale_picture|mnf_enable_hot_keys,
   "Borcha leads you out from {s3} before dawn, not on the road but beside it. A caravan hand's warning proves true: brush cut low, stones moved for wheels, and a place where riders can appear as if the ground spat them out.^^Borcha grins without warmth. 'Road keeps secrets. Today it keeps ours.'",
   "none",
    [
      (set_background_mesh, "mesh_pic_bandits"),
      (try_begin),
        (is_between, "$g_sod_borcha_road_origin_center", towns_begin, towns_end),
        (str_store_party_name_link, s3, "$g_sod_borcha_road_origin_center"),
      (else_try),
        (str_store_string, s3, "@the road town"),
      (try_end),
    ],
    [
      ("borcha_counter_ambush_fight", [
          (main_party_has_troop, "trp_npc1"),
          (eq, "$g_sod_borcha_road_pending", 1),
          (eq, "$g_sod_borcha_road_witnessed", 1),
          (eq, "$g_sod_borcha_road_confronted", 0),
        ], "Spring the counter-ambush with Borcha.",
        [
          (party_get_slot, ":scene_to_use", "$g_sod_borcha_road_origin_center", slot_town_center),
          (modify_visitors_at_site, ":scene_to_use"),
          (reset_visitors),
          (set_visitor, 0, "trp_player"),
          (set_visitor, 1, "trp_npc1"),
          (set_visitor, 2, "trp_caravan_guard"),
          (set_visitor, 10, "trp_bandit"),
          (set_visitor, 11, "trp_brigand"),
          (set_visitor, 12, "trp_henchman"),
          (set_visitor, 13, "trp_bandit"),
          (set_jump_mission, "mt_companion_borcha_counter_ambush"),
          (jump_to_scene, ":scene_to_use"),
          (change_screen_mission),
        ]
      ),
      ("borcha_counter_ambush_bypass", [
          (main_party_has_troop, "trp_npc1"),
          (eq, "$g_sod_borcha_road_pending", 1),
          (eq, "$g_sod_borcha_road_witnessed", 1),
          (eq, "$g_sod_borcha_road_confronted", 0),
        ], "Use Borcha's side path to lead travelers around the trap.",
        [
          (assign, "$g_sod_borcha_road_confronted", 1),
          (assign, "$g_sod_borcha_road_result_grade", 2),
          (quest_set_slot, "qst_companion_borcha_road_keeps_own", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_borcha_road_keeps_own", slot_quest_sod_runtime_metadata, "$g_sod_borcha_road_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_safe_roadcraft, 2),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc1"),
          (display_message, "@Borcha walks the caravan around the teeth of the trap. The raiders keep their lives; the road loses its secret.", 0xCCCC66),
          (jump_to_menu, "mnu_borcha_road_keeps_own"),
        ]
      ),
      ("borcha_counter_ambush_sell_route", [
          (main_party_has_troop, "trp_npc1"),
          (eq, "$g_sod_borcha_road_pending", 1),
          (eq, "$g_sod_borcha_road_witnessed", 1),
          (eq, "$g_sod_borcha_road_confronted", 0),
        ], "Sell the warning to the richest caravan and leave the rest to learn.",
        [
          (assign, "$g_sod_borcha_road_confronted", 1),
          (assign, "$g_sod_borcha_road_result_grade", 1),
          (quest_set_slot, "qst_companion_borcha_road_keeps_own", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_borcha_road_keeps_own", slot_quest_sod_runtime_metadata, "$g_sod_borcha_road_result_grade"),
          (call_script, "script_troop_add_gold", "trp_player", 150),
          (call_script, "script_sod_companion_shift_approval", "trp_npc1", -2),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc1"),
          (display_message, "@The warning sells well. Borcha watches the road afterward, counting who was not worth warning.", 0xCC9966),
          (jump_to_menu, "mnu_borcha_road_keeps_own"),
        ]
      ),
      ("borcha_counter_ambush_leave", [], "Return to town.",
        [
          (jump_to_menu, "mnu_town"),
        ]
      ),
    ]
  ),

("borcha_road_ambush_succeeded", mnf_scale_picture|mnf_enable_hot_keys,
   "The ambushers break against a trap they thought was theirs. Borcha steps over the old wheel ruts and kicks loose the stones that would have pinned the next caravan in place.",
   "none",
    [
      (set_background_mesh, "mesh_pic_bandits"),
      (assign, "$g_sod_borcha_road_confronted", 1),
      (try_begin),
        (le, "$g_sod_borcha_road_result_grade", 0),
        (assign, "$g_sod_borcha_road_result_grade", 3),
      (try_end),
      (quest_set_slot, "qst_companion_borcha_road_keeps_own", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_borcha_road_keeps_own", slot_quest_sod_runtime_metadata, "$g_sod_borcha_road_result_grade"),
      (call_script, "script_sod_companion_apply_player_action", sod_companion_action_safe_roadcraft, 3),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc1"),
    ],
    [
      ("borcha_road_ambush_after", [], "Speak with Borcha about the road.",
        [
          (jump_to_menu, "mnu_borcha_road_keeps_own"),
        ]
      ),
    ]
  ),

("borcha_road_ambush_failed", mnf_scale_picture|mnf_enable_hot_keys,
   "The side road becomes noise and dust. Borcha gets you clear, but his mouth is a hard line: not anger, not fear, just the old memory of a route that ate someone because warning came too late.",
   "none",
    [
      (set_background_mesh, "mesh_pic_bandits"),
      (assign, "$g_sod_borcha_road_confronted", 1),
      (assign, "$g_sod_borcha_road_result_grade", -1),
      (quest_set_slot, "qst_companion_borcha_road_keeps_own", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_borcha_road_keeps_own", slot_quest_sod_runtime_metadata, "$g_sod_borcha_road_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc1"),
    ],
    [
      ("borcha_road_failed_after", [], "Face Borcha's road lesson.",
        [
          (jump_to_menu, "mnu_borcha_road_keeps_own"),
        ]
      ),
    ]
  ),
]
