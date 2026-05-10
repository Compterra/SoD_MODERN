MENUS = [
(
    "town_trade", mnf_enable_hot_keys,
    "You make your way toward the marketplace, where hawkers shout over one another and the smell of leather, oil, and pack animals hangs in the air.",
    "none",
    [
      #(set_background_mesh, "$g_sod_town_background"),
      (set_background_mesh, "mesh_pic_marketplace"),
    ],
    [
      ("trade_with_arms_merchant", [(party_slot_ge, "$current_town", slot_town_weaponsmith, 1)],
       "Browse the weaponsmith's wares.",
       [
           (party_get_slot, ":merchant_troop", "$current_town", slot_town_weaponsmith),
           (change_screen_trade, ":merchant_troop"),
        ]),
      ("trade_with_armor_merchant", [(party_slot_ge, "$current_town", slot_town_armorer, 1)],
       "Browse the armorer's stock.",
       [
           (party_get_slot, ":merchant_troop", "$current_town", slot_town_armorer),
           (change_screen_trade, ":merchant_troop"),
        ]),
      ("trade_with_horse_merchant", [(party_slot_ge, "$current_town", slot_town_horse_merchant, 1)],
       "Inspect the horse trader's mounts.",
       [
           (party_get_slot, ":merchant_troop", "$current_town", slot_town_horse_merchant),
           (change_screen_trade, ":merchant_troop"),
        ]),
      ("trade_with_goods_merchant", [(party_slot_ge, "$current_town", slot_town_merchant, 1)],
       "Trade with the goods merchant.",
       [
           (party_get_slot, ":merchant_troop", "$current_town", slot_town_merchant),
           (change_screen_trade, ":merchant_troop"),
        ]),

      ("sod_auto_sell_companion_spares", [(party_slot_ge, "$current_town", slot_town_weaponsmith, 1),
                                          (call_script, "script_get_count_of_companions"),
                                          (gt, reg0, 0)],
       "Sell low-value spare companion gear.",
       [
           (party_get_slot, ":merchant_troop", "$current_town", slot_town_weaponsmith),
           (call_script, "script_sod_auto_sell_companion_inventory_to_merchant", ":merchant_troop", 300),
           (try_begin),
             (party_slot_ge, "$current_town", slot_town_armorer, 1),
             (party_get_slot, ":merchant_troop", "$current_town", slot_town_armorer),
             (call_script, "script_sod_auto_sell_companion_inventory_to_merchant", ":merchant_troop", 300),
           (try_end),
           (try_begin),
             (party_slot_ge, "$current_town", slot_town_merchant, 1),
             (party_get_slot, ":merchant_troop", "$current_town", slot_town_merchant),
             (call_script, "script_sod_auto_sell_companion_inventory_to_merchant", ":merchant_troop", 300),
           (try_end),
        ]),

      ("sod_auto_sell_companion_spares_broad", [(party_slot_ge, "$current_town", slot_town_weaponsmith, 1),
                                                (call_script, "script_get_count_of_companions"),
                                                (gt, reg0, 0)],
       "Sell ordinary spare companion gear.",
       [
           (party_get_slot, ":merchant_troop", "$current_town", slot_town_weaponsmith),
           (call_script, "script_sod_auto_sell_companion_inventory_to_merchant", ":merchant_troop", 600),
           (try_begin),
             (party_slot_ge, "$current_town", slot_town_armorer, 1),
             (party_get_slot, ":merchant_troop", "$current_town", slot_town_armorer),
             (call_script, "script_sod_auto_sell_companion_inventory_to_merchant", ":merchant_troop", 600),
           (try_end),
           (try_begin),
             (party_slot_ge, "$current_town", slot_town_merchant, 1),
             (party_get_slot, ":merchant_troop", "$current_town", slot_town_merchant),
             (call_script, "script_sod_auto_sell_companion_inventory_to_merchant", ":merchant_troop", 600),
           (try_end),
        ]),

      ("sod_auto_buy_missing_food", [(party_slot_ge, "$current_town", slot_town_merchant, 1)],
       "Buy missing food types.",
       [
           (party_get_slot, ":merchant_troop", "$current_town", slot_town_merchant),
           (call_script, "script_sod_auto_buy_food_from_merchant", ":merchant_troop"),
        ]),

      ("sod_repair_weapons", [(party_slot_ge, "$current_town", slot_town_weaponsmith, 1)],
       "Have damaged weapons repaired.",
       [
           (call_script, "script_sod_repair_player_party_equipment", sod_repair_service_weapons),
        ]),

      ("sod_repair_armor", [(party_slot_ge, "$current_town", slot_town_armorer, 1)],
       "Have battered armor and shields repaired.",
       [
           (call_script, "script_sod_repair_player_party_equipment", sod_repair_service_armor),
        ]),

      ("sod_repair_horses", [(party_slot_ge, "$current_town", slot_town_horse_merchant, 1)],
       "Have injured mounts cared for.",
       [
           (call_script, "script_sod_repair_player_party_equipment", sod_repair_service_horses),
        ]),

      ("assess_prices", [],
        "Survey the local prices...",
        [
          (jump_to_menu, "mnu_town_trade_assessment_begin"),
        ]
      ),
	  
	  ("upgrade", [
        (eq, "$sneaked_into_town", 0),
		],
        "Review your soldiers for promotion.",
        [
		  (assign, "$jump_menu", "mnu_town_trade"),
          (jump_to_menu, "mnu_sod_upgrade"),
        ]
      ),

      # Jedediah Q's Companions Overview
      ("Companions_overview",
        [
          (call_script, "script_get_count_of_companions"),
          (gt, reg0, 0),
        ],
        "Review my companions.",
        [
          # player is in market menu
          (assign, "$jq_in_market_menu", 1),
          (start_presentation, "prsnt_jq_companions_quickview"),
        ]
      ),

      # Autoloot from market
      ("market_goto_autoloot",
        [
          (call_script, "script_get_count_of_companions"),
          (gt, reg0, 0),
        ],
        "Inspect my party's equipment.",
        [
          (troop_clear_inventory, "trp_temp_troop"),
          (assign, "$return_menu", "mnu_town_trade"),
          (assign, "$inventory_menu_offset", 0),
          (str_clear, s30),
          (jump_to_menu, "mnu_manage_loot_pool")
        ]
      ),

      ("back_to_town_menu", [], "Return to the streets.", [ (jump_to_menu, "mnu_town"), ]),
    ]
  ),
]
