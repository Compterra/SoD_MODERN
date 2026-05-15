MENUS = [
(
    "start_phase_2", mnf_disable_all_keys,
    "You arrive in Calradia, a land torn between rival kingdoms battling for supremacy:"\
    " a haven for knights and mercenaries, cutthroats and adventurers, all willing to risk their lives in pursuit of fortune, power, or glory..."\
    " In this land of great danger and even greater opportunity, you will leave your past behind and begin a new life."\
    " Now, on a rise above a distant village, you feel that you hold the key to your destiny, free to choose as you will,"\
    " and that whatever course you take, great adventure awaits!",
    "none",
    [
      (set_background_mesh, "mesh_pic_chr7_arrived"),
    ],
    [
      ("continue", [], "Continue...",
       [
         (assign, "$g_sod_initial_world_setup_pending", 0),
         (assign, "$g_sod_description_return_to_reports", 0),
         (call_script, "script_get_player_party_morale_values"),
         (party_set_morale, "p_main_party", reg0),
         (assign, "$g_sod_player_world_ready", 1),
         (assign, "$g_player_party_icon", -1),
         (assign, "$g_sod_player_map_icon_dirty", 1),
         (call_script, "script_sod_refresh_player_map_icon"),
         (change_screen_return),
        ]
       ),
    ]
  ),
]
