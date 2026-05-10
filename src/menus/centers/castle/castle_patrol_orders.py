MENUS = [
("castle_patrol_orders", mnf_enable_hot_keys,
   "{s9}",
   "none",
   [
     (set_background_mesh, "mesh_pic_castle_1_inside"),
     (call_script, "script_sod_store_castle_patrol_order_report", "$current_town"),
   ],
   [
     ("castle_patrol_commission_road", [
        (call_script, "script_sod_player_can_order_castle_patrols", "$current_town"),
        (eq, reg0, 1),
      ], "Commission a road patrol.", [
        (call_script, "script_sod_player_commission_castle_patrol", "$current_town", sod_castle_patrol_role_road, 0),
        (jump_to_menu, "mnu_castle_patrol_orders"),
      ]),
     ("castle_patrol_commission_village", [
        (call_script, "script_sod_player_can_order_castle_patrols", "$current_town"),
        (eq, reg0, 1),
      ], "Guard bound villages.", [
        (call_script, "script_sod_player_commission_castle_patrol", "$current_town", sod_castle_patrol_role_village_shield, 0),
        (jump_to_menu, "mnu_castle_patrol_orders"),
      ]),
     ("castle_patrol_commission_border", [
        (call_script, "script_sod_player_can_order_castle_patrols", "$current_town"),
        (eq, reg0, 1),
        (store_faction_of_party, ":castle_faction", "$current_town"),
        (assign, ":at_war", 0),
        (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
          (store_relation, ":relation", ":castle_faction", ":faction_no"),
          (lt, ":relation", 0),
          (assign, ":at_war", 1),
        (try_end),
        (eq, ":at_war", 1),
      ], "Harass the border.", [
        (call_script, "script_sod_player_commission_castle_patrol", "$current_town", sod_castle_patrol_role_border_harasser, 0),
        (jump_to_menu, "mnu_castle_patrol_orders"),
      ]),
     ("castle_patrol_commission_caravan", [
        (call_script, "script_sod_player_can_order_castle_patrols", "$current_town"),
        (eq, reg0, 1),
      ], "Screen caravans.", [
        (call_script, "script_sod_player_commission_castle_patrol", "$current_town", sod_castle_patrol_role_caravan_screen, 0),
        (jump_to_menu, "mnu_castle_patrol_orders"),
      ]),
     ("castle_patrol_commission_campaign", [
        (call_script, "script_sod_player_can_order_castle_patrols", "$current_town"),
        (eq, reg0, 1),
      ], "Support the marshal campaign.", [
        (call_script, "script_sod_player_commission_castle_patrol", "$current_town", sod_castle_patrol_role_campaign_screen, 0),
        (jump_to_menu, "mnu_castle_patrol_orders"),
      ]),
     ("castle_patrol_fund_quality", [
        (call_script, "script_sod_player_can_order_castle_patrols", "$current_town"),
        (eq, reg0, 1),
        (store_troop_gold, ":gold", "trp_player"),
        (ge, ":gold", 500),
      ], "Fund an extra-quality road patrol. Costs 500 denars.", [
        (call_script, "script_sod_player_commission_castle_patrol", "$current_town", sod_castle_patrol_role_road, 1),
        (jump_to_menu, "mnu_castle_patrol_orders"),
      ]),
     ("castle_patrol_recall", [
        (call_script, "script_sod_player_can_order_castle_patrols", "$current_town"),
        (eq, reg0, 1),
      ], "Recall active patrols.", [
        (call_script, "script_sod_player_recall_castle_patrols", "$current_town"),
        (jump_to_menu, "mnu_castle_patrol_orders"),
      ]),
     ("castle_patrol_redirect", [
        (call_script, "script_sod_player_can_order_castle_patrols", "$current_town"),
        (eq, reg0, 1),
      ], "Redirect active patrols to the nearest road endpoint.", [
        (call_script, "script_sod_player_redirect_castle_patrols", "$current_town"),
        (jump_to_menu, "mnu_castle_patrol_orders"),
      ]),
     ("castle_patrol_back", [], "Back.", [(jump_to_menu, "mnu_town")]),
   ]
 ),
]
