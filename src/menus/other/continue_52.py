MENUS = [
(
    "captivity_end_exchanged_with_prisoner", 0,
    "After days of imprisonment, you are finally set free when your captors exchange you with another prisoner.",
    "none",
    [
      (play_cue_track, "track_escape"),
      ],
    [
      ("continue", [], "Continue...",
       [
           (assign, "$g_player_is_captive", 0),
           (try_begin),
             (party_is_active, "$capturer_party"),
             (party_relocate_near_party, "p_main_party", "$capturer_party", 2),
           (try_end),
           (call_script, "script_set_parties_around_player_ignore_player", 2, 12),
           (assign, "$g_player_icon_state", pis_normal),
           (call_script, "script_sod_refresh_player_map_icon"),
           (set_camera_follow_party, "p_main_party"),
           (rest_for_hours, 0, 0, 0), #stop resting
           (change_screen_return),
        ]),
    ]
  ),
]
