MENUS = [
(
    "captivity_end_wilderness_escape", mnf_scale_picture,
    "After painful days of being dragged about as a prisoner, you find a chance and escape from your captors!",
    "none",
    [
        (play_cue_track, "track_escape"),
        (troop_get_type, ":is_female", "trp_player"),
        (try_begin),
          (eq, ":is_female", 1),
          (set_background_mesh, "mesh_pic_escape_1_fem"),
        (else_try),
          (set_background_mesh, "mesh_pic_escape_1"),
        (try_end),
    ],
    [
      ("continue", [], "Continue...",
       [
           (assign, "$g_player_is_captive", 0),
           (try_begin),
             (party_is_active, "$capturer_party"),
             (party_relocate_near_party, "p_main_party", "$capturer_party", 2),
           (try_end),
           (call_script, "script_set_parties_around_player_ignore_player", 2, 4),
           (assign, "$g_player_icon_state", pis_normal),
           (set_camera_follow_party, "p_main_party"),
           (rest_for_hours, 0, 0, 0), #stop resting
           (change_screen_return),
        ]),
    ]
  ),
]
