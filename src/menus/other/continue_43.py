MENUS = [
(
    "town_trade_assessment_begin", mnf_enable_hot_keys,
    "You overhear several discussions about the price of trade goods across the local area. You listen closely, trying to work out the best deals around.",
    "none",
    [
      (set_background_mesh, "$g_sod_town_background"),
    ],
    [
      ("continue", [], "Continue...",
        [
          (assign, "$auto_enter_town", "$current_town"),
          (assign, "$g_town_assess_trade_goods_after_rest", 1),
          (call_script, "script_get_max_skill_of_player_party", "skl_trade"),
          (val_div, reg0, 2),
          (store_sub, ":num_hours", 6, reg0),
          (assign, "$g_last_rest_center", "$current_town"),
          (assign, "$g_last_rest_payment_until", -1),
          (rest_for_hours, ":num_hours", 5, 0), #rest while not attackable
          (change_screen_return),
        ]
      ),
	  ("back_to_town_menu", [], "Head back.", [ (jump_to_menu, "mnu_town"), ]),
    ]
  ),
]
