MENUS = [
(
    "captivity_end_propose_ransom", 0,
    "You spend long hours in the sunless dank of the dungeon, more than you can count. Suddenly one of your captors enters your cell with an offer. He proposes to free you in return for {reg5} denars of your hidden wealth. You decide to...",
    "none",
    [
        (try_begin),
          (le, "$player_ransom_amount", 0),
          (store_character_level, ":player_level", "trp_player"),
          (store_mul, "$player_ransom_amount", ":player_level", 50),
          (val_add, "$player_ransom_amount", 100),
        (try_end),
        (assign, reg5, "$player_ransom_amount"),
    ],
    [
      ("captivity_end_ransom_accept", [(store_troop_gold, ":player_gold", "trp_player"),
                                      (ge, ":player_gold", "$player_ransom_amount")], "Accept the offer.",
       [
           (play_cue_track, "track_escape"),
           (assign, "$g_player_is_captive", 0),
           (call_script, "script_sod_player_charge_gold", "$player_ransom_amount"),
           (assign, "$player_ransom_amount", 0),
           (call_script, "script_sod_validate_capturer_party_to_reg"),
           (call_script, "script_sod_runtime_trace_event", 4, "$capturer_party", "trp_player"),
           (try_begin),
             (eq, reg0, 1),
             (party_relocate_near_party, "p_main_party", "$capturer_party", 1),
           (try_end),
           (call_script, "script_sod_sanitize_encounter_globals"),
           (call_script, "script_set_parties_around_player_ignore_player", 2, 6),
           (assign, "$g_player_icon_state", pis_normal),
           (call_script, "script_sod_refresh_player_map_icon"),
           (set_camera_follow_party, "p_main_party"),
           (rest_for_hours, 0, 0, 0), #stop resting
           (change_screen_return),
        ]),
      ("captivity_end_ransom_deny", [], "Refuse him, wait for something better.",
       [
           (assign, "$g_player_is_captive", 1),
           (store_random_in_range, reg(8), 16, 22),
           (call_script, "script_stay_captive_for_hours", reg8),
           (assign, "$auto_menu", "mnu_captivity_castle_check"),
           (change_screen_return),
        ]),
    ]
  ),
]
