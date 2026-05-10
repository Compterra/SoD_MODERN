MENUS = [
(
    "start_phase_2", mnf_disable_all_keys,
    "You arrive at Calradia, a land torn between rival kingdoms battling each other for supremacy,"\
    " a haven for knights and mercenaries, cutthroats and adventurers, all willing to risk their lives in pursuit of fortune, power, or glory..."\
    " In this land which holds great dangers and even greater opportunities, you will leave your past behind and start a new life."\
    " Now, on a rise above a distant village, you feel that you hold the key of your destiny in your hands, free to choose as you will,"\
    " and that whatever course you take, great adventure awaits you!",
    "none",
    [
      (set_background_mesh, "mesh_pic_chr7_arrived"),
    ],
    [
      ("continue", [], "Continue...",
       [
         (assign, "$g_sod_initial_world_setup_pending", 1),
         (assign, "$g_sod_description_return_to_reports", 0),
         (change_screen_return),
        ]
       ),
    ]
  ),
]
