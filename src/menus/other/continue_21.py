MENUS = [
(
    "recruit_volunteers", 0,
    "{s18}",
    "none",
    [
      # determine what & count
      (call_script, "script_village_recruit_volunteers_get_params", 0),
      (assign, ":volunteer_troop", reg0),
      (assign, ":volunteer_amount", reg1),

      (assign, reg5, ":volunteer_amount"),

      (try_begin),
        (eq, ":volunteer_amount", 0),
        (str_store_string, s18, "@No one here seems to be willing to join your party."),
      (else_try),
        (store_mul, reg6, ":volunteer_amount", 10), #10 denars per man
        (str_store_troop_name_by_count, s3, ":volunteer_troop", ":volunteer_amount"),
        (try_begin),
          (eq, reg5, 1),
          (str_store_string, s18, "@One peasant volunteers to follow you."),
        (else_try),
          (str_store_string, s18, "@{reg5} peasants volunteer to follow you."),
        (try_end),
        (set_background_mesh, "mesh_pic_recruits"),
      (try_end),
    ],
    [
      ("continue", [(eq, reg5, 0)], "Continue...", [(party_set_slot, "$current_town", slot_center_volunteer_troop_amount, -1), (jump_to_menu, "mnu_village")]),
      ("recruit_them", [(gt, reg5, 0)], "Recruit them as native recruits. ({reg6} denars)", [(call_script, "script_village_recruit_volunteers_recruit", 0), (jump_to_menu, "mnu_village"), ]),
      ("recruit_mercenaries", [(gt, reg5, 0)], "Recruit them as mercenaries. ({reg6} denars)", [(call_script, "script_village_recruit_volunteers_recruit", 1), (jump_to_menu, "mnu_village"), ]),
      ("recruit_special", [(gt, reg5, 0), 
	  (call_script, "script_village_recruit_volunteers_get_params", 2),
      (str_store_troop_name_by_count, s3, reg0, 2),
	  ], "Recruit them as {s3}. ({reg6} denars)", [(call_script, "script_village_recruit_volunteers_recruit", 2), (jump_to_menu, "mnu_village"), ]),
      ("forget_it", [(gt, reg5, 0)], "Forget it.", [(jump_to_menu, "mnu_village")]),
    ],
  ),
]
