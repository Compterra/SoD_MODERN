MENUS = [
(
    "zendar", mnf_auto_enter,
    "You enter the town of Zendar.",
    "none",
    [(reset_price_rates, 0), (set_price_rate_for_item, "itm_tools", 70), (set_price_rate_for_item, "itm_salt", 140)],
    [
      ("zendar_enter", [], "_", [(set_jump_mission, "mt_town_default"), (jump_to_scene, "scn_zendar_center"), (change_screen_mission)], "Door to the town center."),
      ("zendar_tavern", [], "_", [(set_jump_mission, "mt_town_default"),
                                                   (jump_to_scene, "scn_the_happy_boar"),
                                                   (change_screen_mission)], "Door to the tavern."),
      ("zendar_merchant", [], "_", [(set_jump_mission, "mt_town_default"),
                                                   (jump_to_scene, "scn_zendar_merchant"),
                                                   (change_screen_mission)], "Door to the merchant."),
      ("zendar_arena", [], "_", [(set_jump_mission, "mt_town_default"),
                                                   (jump_to_scene, "scn_zendar_arena"),
                                                   (change_screen_mission)], "Door to the arena."),
#      ("zendar_leave", [], "Leave town.", [[leave_encounter], [change_screen_return]]),
      ("town_1_leave", [], "_", [(leave_encounter), (change_screen_return)]),
    ]
  ),
]
