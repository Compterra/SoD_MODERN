MENUS = [
("camp_jobs", mnf_scale_picture|mnf_enable_hot_keys,
   "{s1}",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (call_script, "script_sod_camp_job_describe_to_s1"),
    ],
    [
      ("camp_jobs_rest_passive", [
          (eq, "$g_sod_camp_job_active", 0),
        ], "Rest six hours and let passive camp roles work.",
        [
          (assign, "$g_camp_mode", 1),
          (assign, "$g_player_icon_state", pis_camping),
          (call_script, "script_sod_refresh_player_map_icon"),
          (rest_for_hours_interactive, 6, 5, 1),
          (change_screen_return),
        ]
      ),

      ("camp_job_scout_route", [
          (eq, "$g_sod_camp_job_active", 0),
          (main_party_has_troop, "trp_npc1"),
        ], "Direct order: scout the route for six hours.",
        [
          (assign, "$g_camp_mode", 1),
          (assign, "$g_player_icon_state", pis_camping),
          (call_script, "script_sod_refresh_player_map_icon"),
          (call_script, "script_sod_camp_job_start", sod_camp_job_scout_route, 6, "trp_npc1"),
          (try_begin),
            (eq, reg0, 1),
            (rest_for_hours_interactive, 6, 5, 1),
            (change_screen_return),
          (else_try),
            (display_message, "@No camp job was started.", 0xFFCC66),
            (jump_to_menu, "mnu_camp_jobs"),
          (try_end),
        ]
      ),

      ("camp_job_scout_route_locked", [
          (eq, "$g_sod_camp_job_active", 0),
          (neg|main_party_has_troop, "trp_npc1"),
        ], "Direct order: scout the route. Requires Borcha.",
        [
          (display_message, "@You need Borcha in the party to post a proper road watch.", 0xFFCC66),
          (jump_to_menu, "mnu_camp_jobs"),
        ]
      ),

      ("camp_job_forage_hunt", [
          (eq, "$g_sod_camp_job_active", 0),
        ], "Direct order: forage and hunt for six hours.",
        [
          (assign, "$g_camp_mode", 1),
          (assign, "$g_player_icon_state", pis_camping),
          (call_script, "script_sod_refresh_player_map_icon"),
          (call_script, "script_sod_camp_job_start", sod_camp_job_forage_hunt, 6, "trp_player"),
          (try_begin),
            (eq, reg0, 1),
            (rest_for_hours_interactive, 6, 5, 1),
            (change_screen_return),
          (else_try),
            (display_message, "@No camp job was started.", 0xFFCC66),
            (jump_to_menu, "mnu_camp_jobs"),
          (try_end),
        ]
      ),

      ("camp_job_ration_stores", [
          (eq, "$g_sod_camp_job_active", 0),
          (main_party_has_troop, "trp_npc2"),
        ], "Direct order: have Marnid count and sort stores for six hours.",
        [
          (assign, "$g_camp_mode", 1),
          (assign, "$g_player_icon_state", pis_camping),
          (call_script, "script_sod_refresh_player_map_icon"),
          (call_script, "script_sod_camp_job_start", sod_camp_job_ration_stores, 6, "trp_npc2"),
          (try_begin),
            (eq, reg0, 1),
            (rest_for_hours_interactive, 6, 5, 1),
            (change_screen_return),
          (else_try),
            (display_message, "@No camp job was started.", 0xFFCC66),
            (jump_to_menu, "mnu_camp_jobs"),
          (try_end),
        ]
      ),

      ("camp_job_ration_stores_locked", [
          (eq, "$g_sod_camp_job_active", 0),
          (neg|main_party_has_troop, "trp_npc2"),
        ], "Direct order: count and sort stores. Requires Marnid.",
        [
          (display_message, "@You need Marnid in the party to organize the camp stores.", 0xFFCC66),
          (jump_to_menu, "mnu_camp_jobs"),
        ]
      ),

      ("camp_job_tend_mounts", [
          (eq, "$g_sod_camp_job_active", 0),
          (main_party_has_troop, "trp_npc5"),
        ], "Direct order: have Baheshtur tend the mounts for six hours.",
        [
          (assign, "$g_camp_mode", 1),
          (assign, "$g_player_icon_state", pis_camping),
          (call_script, "script_sod_refresh_player_map_icon"),
          (call_script, "script_sod_camp_job_start", sod_camp_job_tend_mounts, 6, "trp_npc5"),
          (try_begin),
            (eq, reg0, 1),
            (rest_for_hours_interactive, 6, 5, 1),
            (change_screen_return),
          (else_try),
            (display_message, "@No camp job was started.", 0xFFCC66),
            (jump_to_menu, "mnu_camp_jobs"),
          (try_end),
        ]
      ),

      ("camp_job_tend_mounts_locked", [
          (eq, "$g_sod_camp_job_active", 0),
          (neg|main_party_has_troop, "trp_npc5"),
        ], "Direct order: tend the mounts. Requires Baheshtur.",
        [
          (display_message, "@You need Baheshtur in the party to tend lame mounts.", 0xFFCC66),
          (jump_to_menu, "mnu_camp_jobs"),
        ]
      ),

      ("camp_job_repair_gear", [
          (eq, "$g_sod_camp_job_active", 0),
        ], "Direct order: repair gear for six hours.",
        [
          (assign, "$g_camp_mode", 1),
          (assign, "$g_player_icon_state", pis_camping),
          (call_script, "script_sod_refresh_player_map_icon"),
          (call_script, "script_sod_camp_job_start", sod_camp_job_repair_gear, 6, "trp_player"),
          (try_begin),
            (eq, reg0, 1),
            (rest_for_hours_interactive, 6, 5, 1),
            (change_screen_return),
          (else_try),
            (display_message, "@No camp job was started.", 0xFFCC66),
            (jump_to_menu, "mnu_camp_jobs"),
          (try_end),
        ]
      ),

      ("camp_job_abandon", [
          (eq, "$g_sod_camp_job_active", 1),
        ], "Break off the current camp job.",
        [
          (assign, "$g_sod_camp_job_last_result", sod_camp_job_result_cancelled),
          (call_script, "script_sod_camp_job_clear"),
          (display_message, "@The current camp job is cancelled.", 0xFFCC66),
          (jump_to_menu, "mnu_camp_jobs"),
        ]
      ),

      ("camp_jobs_back", [], "Return to camp actions.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),
]
