MENUS = [
("camp", mnf_scale_picture|mnf_enable_hot_keys,
   "You set up camp. What do you want to do?",
   "none",
   [
     (assign, "$g_player_icon_state", pis_camping),
     (call_script, "script_sod_refresh_player_map_icon"),
     # Clear stale center or party ids before opening camp; old encounter globals
     # can point at removed parties and crash later camp/report menus.
     (try_begin),
       (gt, "$g_encountered_party", 0),
       (neg|party_is_active, "$g_encountered_party"),
       (assign, "$g_encountered_party", -1),
     (try_end),
     (try_begin),
       (gt, "$g_encountered_party_2", 0),
       (neg|party_is_active, "$g_encountered_party_2"),
       (assign, "$g_encountered_party_2", -1),
     (try_end),
     (try_begin),
       (gt, "$current_town", 0),
       (neg|party_is_active, "$current_town"),
       (assign, "$current_town", -1),
     (try_end),
     (set_background_mesh, "mesh_pic_camp"),
    ],
    [

      ("kingdom_management", [(eq, "$g_sod_king", 1)], "Kingdom Management.", [(jump_to_menu, "mnu_kingdom_management")]),
      ("party_management", [], "Party Management.", [(jump_to_menu, "mnu_party_management")]),

      ("camp_wait_here", [], "Rest here for some time...",
       [
           (assign, "$g_camp_mode", 1),
           (assign, "$g_player_icon_state", pis_camping),
           (call_script, "script_sod_refresh_player_map_icon"),
           (rest_for_hours_interactive, 24 * 7, 5, 1), #rest while attackable
           (change_screen_return),
        ]
       ),
      ("camp_action", [], "Take other action...", [(jump_to_menu, "mnu_camp_action")]),

      ("resume_travelling", [], "Resume travelling.",
       [
         (assign, "$g_player_icon_state", pis_normal),
         (call_script, "script_sod_refresh_player_map_icon"),
         (change_screen_return),
       ]), ]
  ),
]
