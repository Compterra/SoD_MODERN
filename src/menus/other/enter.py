MENUS = [
(
    "salt_mine", mnf_auto_enter,
    "You enter the salt mine. The air turns dry and bitter on your tongue, and every sound comes back from the tunnels in a dull, chalk-white echo.",
    "none",
    [(reset_price_rates, 0), (set_price_rate_for_item, "itm_salt", 55)],
    [
      ("enter", [], "Descend into the mine.", [(set_jump_mission, "mt_town_center"), (jump_to_scene, "scn_salt_mine"), (change_screen_mission)]),
      ("leave", [], "Leave.", [(leave_encounter), (change_screen_return)]),
    ]
  ),
]
