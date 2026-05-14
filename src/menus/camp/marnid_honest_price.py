MENUS = [
("marnid_honest_price", mnf_scale_picture|mnf_enable_hot_keys,
   "Marnid opens the contract again. The clean columns are still clean. That is what bothers him. Names are missing where labor should be named, debt appears where wages should stand, and the merchant's witness has pointed toward a locked storehouse in {s3}.^^The contract has shown its cost. Now Marnid waits to see whether the company pays it honestly.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (try_begin),
        (this_or_next|neg|main_party_has_troop, "trp_npc2"),
        (neq, "$g_sod_marnid_market_pending", 1),
        (assign, "$g_sod_marnid_market_pending", 0),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (is_between, "$g_sod_marnid_market_focus_center", towns_begin, towns_end),
        (str_store_party_name_link, s3, "$g_sod_marnid_market_focus_center"),
      (else_try),
        (str_store_string, s3, "@the market town"),
      (try_end),
    ],
    [
      ("marnid_price_expose", [
          (main_party_has_troop, "trp_npc2"),
          (ge, "$g_sod_marnid_market_evidence", 1),
          (eq, "$g_sod_marnid_market_confronted", 1),
        ], "Expose the dirty contract and pay compensation from the seized goods.",
        [
          (assign, "$g_sod_marnid_market_pending", 0),
          (assign, "$g_sod_marnid_market_result_grade", 3),
          (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_metadata, "$g_sod_marnid_market_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_orderly_profit, 3),
          (call_script, "script_sod_companion_shift_core_value_proof", "trp_npc2", 2),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc2", 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc2"),
          (display_message, "@Marnid balances the last page and smiles despite himself. 'A rare thing: profit that does not need hiding.'", 0x99CCFF),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("marnid_price_repay", [
          (main_party_has_troop, "trp_npc2"),
          (ge, "$g_sod_marnid_market_evidence", 1),
          (eq, "$g_sod_marnid_market_confronted", 1),
          (store_troop_gold, ":gold", "trp_player"),
          (ge, ":gold", 300),
        ], "Repay the cheated laborers and keep the clean part of the contract.",
        [
          (assign, "$g_sod_marnid_market_pending", 0),
          (assign, "$g_sod_marnid_market_result_grade", 2),
          (call_script, "script_sod_player_charge_gold", 300),
          (eq, reg1, 1),
          (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_metadata, "$g_sod_marnid_market_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_orderly_profit, 2),
          (call_script, "script_sod_companion_shift_approval", "trp_npc2", 2),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc2", 1),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc2"),
          (display_message, "@The books still show profit, but now they also show names. Marnid calls that the difference between trade and theft.", 0xCCCC66),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("marnid_price_leverage", [
          (main_party_has_troop, "trp_npc2"),
          (ge, "$g_sod_marnid_market_evidence", 1),
          (eq, "$g_sod_marnid_market_confronted", 1),
        ], "Use the evidence for leverage and take the discount.",
        [
          (assign, "$g_sod_marnid_market_pending", 0),
          (assign, "$g_sod_marnid_market_result_grade", 1),
          (call_script, "script_troop_add_gold", "trp_player", 300),
          (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_metadata, "$g_sod_marnid_market_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_dirty_profit, 2),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc2", 0),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc2"),
          (troop_set_slot, "trp_npc2", slot_troop_companion_warning_state, sod_companion_warning_pending),
          (display_message, "@The profit is real. So is Marnid's silence when he counts it.", 0xCC9966),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("marnid_price_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("marnid_price_warehouse", mnf_scale_picture|mnf_enable_hot_keys,
   "The warehouse behind the market is too quiet for a place with so many full ledgers. Marnid points at seals scraped from crates and names rewritten in a steadier hand than fear could manage.^^The guard at the door says the contract is legal. Marnid says legality is often where theft buys a chair.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("marnid_warehouse_force", [
          (main_party_has_troop, "trp_npc2"),
          (eq, "$g_sod_marnid_market_pending", 1),
          (ge, "$g_sod_marnid_market_evidence", 1),
          (eq, "$g_sod_marnid_market_confronted", 0),
        ], "Force the warehouse open and protect the witnesses.",
        [
          (party_get_slot, ":scene_to_use", "$g_sod_marnid_market_focus_center", slot_town_center),
          (modify_visitors_at_site, ":scene_to_use"),
          (reset_visitors),
          (set_visitor, 0, "trp_player"),
          (set_visitor, 1, "trp_npc2"),
          (set_visitor, 2, "trp_caravan_guard"),
          (set_visitor, 10, "trp_hired_blade"),
          (set_visitor, 11, "trp_watchman"),
          (set_visitor, 12, "trp_henchman"),
          (set_jump_mission, "mt_companion_marnid_warehouse"),
          (jump_to_scene, ":scene_to_use"),
          (change_screen_mission),
        ]
      ),
      ("marnid_warehouse_audit", [
          (main_party_has_troop, "trp_npc2"),
          (eq, "$g_sod_marnid_market_pending", 1),
          (ge, "$g_sod_marnid_market_evidence", 1),
          (eq, "$g_sod_marnid_market_confronted", 0),
        ], "Let Marnid audit the books in public before blades come out.",
        [
          (assign, "$g_sod_marnid_market_confronted", 1),
          (assign, "$g_sod_marnid_market_result_grade", 2),
          (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_metadata, "$g_sod_marnid_market_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_orderly_profit, 2),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc2"),
          (display_message, "@Marnid reads the false accounts aloud until the warehouse guard discovers there is no clean answer left.", 0xCCCC66),
          (jump_to_menu, "mnu_marnid_honest_price"),
        ]
      ),
      ("marnid_warehouse_blackmail", [
          (main_party_has_troop, "trp_npc2"),
          (eq, "$g_sod_marnid_market_pending", 1),
          (ge, "$g_sod_marnid_market_evidence", 1),
          (eq, "$g_sod_marnid_market_confronted", 0),
        ], "Threaten exposure unless the merchant cuts you in.",
        [
          (assign, "$g_sod_marnid_market_confronted", 1),
          (assign, "$g_sod_marnid_market_result_grade", 1),
          (call_script, "script_troop_add_gold", "trp_player", 150),
          (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_metadata, "$g_sod_marnid_market_result_grade"),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_dirty_profit, 1),
          (call_script, "script_sod_companion_shift_approval", "trp_npc2", -2),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc2"),
          (display_message, "@The merchant pays for silence. Marnid writes the number down because ugly accounts still need accuracy.", 0xCC9966),
          (jump_to_menu, "mnu_marnid_honest_price"),
        ]
      ),
      ("marnid_warehouse_leave", [], "Return to town.",
        [
          (jump_to_menu, "mnu_town"),
        ]
      ),
    ]
  ),

("marnid_warehouse_succeeded", mnf_scale_picture|mnf_enable_hot_keys,
   "The warehouse guards fold, then run. Marnid does not chase them. He goes to the crates, the wage marks, and the names hidden under debt numbers.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_marnid_market_confronted", 1),
      (try_begin),
        (le, "$g_sod_marnid_market_result_grade", 0),
        (assign, "$g_sod_marnid_market_result_grade", 3),
      (try_end),
      (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_metadata, "$g_sod_marnid_market_result_grade"),
      (call_script, "script_sod_companion_apply_player_action", sod_companion_action_orderly_profit, 2),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc2"),
    ],
    [
      ("marnid_warehouse_after", [], "Speak with Marnid about the contract.",
        [
          (jump_to_menu, "mnu_marnid_honest_price"),
        ]
      ),
    ]
  ),

("marnid_warehouse_failed", mnf_scale_picture|mnf_enable_hot_keys,
   "The warehouse door slams shut behind the wrong people. Marnid gets the ledger scrap out, but not the witnesses. His hand stays flat on the page as if he can keep the numbers from running.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_marnid_market_confronted", 1),
      (assign, "$g_sod_marnid_market_result_grade", -1),
      (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_marnid_honest_price", slot_quest_sod_runtime_metadata, "$g_sod_marnid_market_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc2"),
    ],
    [
      ("marnid_warehouse_failed_after", [], "Face Marnid's account of the loss.",
        [
          (jump_to_menu, "mnu_marnid_honest_price"),
        ]
      ),
    ]
  ),
]
