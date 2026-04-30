MENUS = [
(
    "kill_local_merchant_begin", 0,
    "You spot your victim and follow him, observing as he turns a corner into a dark alley. This will surely be your best opportunity to attack him.",
    "none",
    [
    ],
    [
      ("continue", [], "Continue...",
       [(set_jump_mission, "mt_back_alley_kill_local_merchant"),
        (party_get_slot, ":town_alley", "$qst_kill_local_merchant_center", slot_town_alley),
        (modify_visitors_at_site, ":town_alley"),
        (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (set_visitor, 1, "trp_local_merchant"),
        (jump_to_menu, "mnu_town"),
        (jump_to_scene, ":town_alley"),
        (change_screen_mission),
        ]),
     ]
  ),
]
