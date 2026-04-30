MENUS = [
(
    "order_attack_begin", mnf_enable_hot_keys,
    "Your troops prepare to attack the enemy.",
    "none",
    [
      (set_background_mesh, "mesh_pic_attack_ready"),
    ],
    [
      ("order_attack_begin", [], "Order the attack to begin.", [
        (assign, "$g_engaged_enemy", 1),
        (jump_to_menu, "mnu_order_attack_2"),
      ]),
      ("call_back", [], "Call them back.", [(jump_to_menu, "mnu_simple_encounter")]),
    ]
  ),
]
