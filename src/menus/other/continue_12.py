MENUS = [
(
    "castle_meeting_selected", mnf_enable_hot_keys,
    "Your request for a meeting is relayed inside, and finally {s6} appears in the courtyard to speak with you.",
    "none",
    [
      (call_script, "script_store_troop_name", s6, "$castle_meeting_selected_troop"),
      (set_background_mesh, "$g_sod_town_background"),
    ],
    [
      ("continue", [],
       "Continue...",
       [(jump_to_menu, "mnu_castle_outside"),
        (modify_visitors_at_site, "scn_conversation_scene"), (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (set_visitor, 17, "$castle_meeting_selected_troop"),
        (set_jump_mission, "mt_conversation_encounter"),
        (jump_to_scene, "scn_conversation_scene"),
        (assign, "$talk_context", tc_castle_gate),
        (change_screen_map_conversation, "$castle_meeting_selected_troop"),
        ]
       ),
    ]
  ),
]
