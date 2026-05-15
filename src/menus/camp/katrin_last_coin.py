MENUS = [
("katrin_last_coin", mnf_scale_picture|mnf_enable_hot_keys,
   "Katrin has set a cup, a cracked ledger, and the last loose coins of the camp on an overturned shield. The company has survived enemies with banners. Now it faces hunger, debt, and the sour little arithmetic that comes after courage.^^{reg1?The men are owed wages, and promises have become thin coin.:The food sacks are light, and supper has become a negotiation.}",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (try_begin),
        (this_or_next|neg|main_party_has_troop, "trp_npc11"),
        (neq, "$g_sod_katrin_last_coin_pending", 1),
        (assign, "$g_sod_katrin_last_coin_pending", 0),
        (assign, "$g_sod_katrin_last_coin_cause", 0),
        (assign, "$g_sod_katrin_last_coin_witnessed", 0),
        (assign, "$g_sod_katrin_last_coin_confronted", 0),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (this_or_next|neq, "$g_sod_katrin_last_coin_witnessed", 1),
        (neq, "$g_sod_katrin_last_coin_confronted", 1),
        (jump_to_menu, "mnu_camp_action"),
      (try_end),
      (try_begin),
        (eq, "$g_sod_katrin_last_coin_cause", 2),
        (assign, reg1, 1),
      (else_try),
        (assign, reg1, 0),
      (try_end),
    ],
    [
      ("katrin_last_coin_stores", [
          (main_party_has_troop, "trp_npc11"),
          (eq, "$g_sod_katrin_last_coin_pending", 1),
          (eq, "$g_sod_katrin_last_coin_witnessed", 1),
          (eq, "$g_sod_katrin_last_coin_confronted", 1),
        ], "Put the coin toward food, medicine, and honest arrears.",
        [
          (assign, "$g_sod_katrin_last_coin_pending", 0),
          (assign, "$g_sod_katrin_last_coin_result_grade", 3),
          (call_script, "script_sod_companion_apply_player_action", sod_companion_action_food_security, 3),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc11", 1),
          (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_metadata, "$g_sod_katrin_last_coin_result_grade"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc11"),
          (call_script, "script_sod_companion_katrin_apply_last_coin_payoff"),
          (display_message, "@Katrin spends without ceremony and saves without romance. The Last Coin in Camp remembers practical care.", 0x99CCFF),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("katrin_last_coin_ration", [
          (main_party_has_troop, "trp_npc11"),
          (eq, "$g_sod_katrin_last_coin_pending", 1),
          (eq, "$g_sod_katrin_last_coin_witnessed", 1),
          (eq, "$g_sod_katrin_last_coin_confronted", 1),
        ], "Stretch the stores hard, but keep the burden shared.",
        [
          (assign, "$g_sod_katrin_last_coin_pending", 0),
          (try_begin),
            (lt, "$g_sod_katrin_last_coin_result_grade", 2),
            (assign, "$g_sod_katrin_last_coin_result_grade", 2),
          (try_end),
          (call_script, "script_sod_companion_shift_approval", "trp_npc11", 2),
          (try_begin),
            (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
            (troop_set_slot, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (else_try),
            (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
            (call_script, "script_sod_companion_advance_personal_quest", "trp_npc11", 1),
            (call_script, "script_sod_companion_katrin_apply_last_coin_payoff"),
          (try_end),
          (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_metadata, "$g_sod_katrin_last_coin_result_grade"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc11"),
          (display_message, "@Katrin makes the rationing fair enough that resentment has fewer places to root.", 0xCCCC66),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("katrin_last_coin_glory", [
          (main_party_has_troop, "trp_npc11"),
          (eq, "$g_sod_katrin_last_coin_pending", 1),
          (eq, "$g_sod_katrin_last_coin_witnessed", 1),
          (eq, "$g_sod_katrin_last_coin_confronted", 1),
        ], "Spend for momentum. The camp can tighten belts later.",
        [
          (assign, "$g_sod_katrin_last_coin_pending", 0),
          (assign, "$g_sod_katrin_last_coin_result_grade", 1),
          (call_script, "script_sod_companion_advance_personal_quest", "trp_npc11", 0),
          (troop_set_slot, "trp_npc11", slot_troop_companion_warning_state, sod_companion_warning_pending),
          (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_progress, 100),
          (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_metadata, "$g_sod_katrin_last_coin_result_grade"),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc11"),
          (display_message, "@The company moves faster today. Katrin makes the thin broth last and says nothing generous about tomorrow.", 0xCC6666),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
      ("katrin_last_coin_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("katrin_supply_watch", mnf_scale_picture|mnf_enable_hot_keys,
   "Katrin has the sacks counted twice: once by ink, once by the eyes of people who will eat from them. A cook holds an empty ladle. A wounded man watches the medicine cloth. A guard keeps looking toward the dark edge of camp.^^'There,' Katrin says. 'That is where command happens. Not in the speech. Beside the sack.'",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("katrin_watch_open_books", [
          (main_party_has_troop, "trp_npc11"),
          (eq, "$g_sod_katrin_last_coin_pending", 1),
          (eq, "$g_sod_katrin_last_coin_witnessed", 1),
          (eq, "$g_sod_katrin_last_coin_confronted", 0),
        ], "Open the books and distribute the burden in public.",
        [
          (assign, "$g_sod_katrin_last_coin_confronted", 1),
          (assign, "$g_sod_katrin_last_coin_result_grade", 3),
          (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_metadata, "$g_sod_katrin_last_coin_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc11", 3),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc11"),
          (display_message, "@The camp sees the sums before it tastes the thin broth. Grumbling remains, but suspicion loses its teeth.", 0x99CCFF),
          (start_map_conversation, "trp_npc11"),
        ]
      ),
      ("katrin_watch_defend_stores", [
          (main_party_has_troop, "trp_npc11"),
          (eq, "$g_sod_katrin_last_coin_pending", 1),
          (eq, "$g_sod_katrin_last_coin_witnessed", 1),
          (eq, "$g_sod_katrin_last_coin_confronted", 0),
        ], "Stand watch when hungry hands test the store line.",
        [
          (modify_visitors_at_site, "scn_random_scene"),
          (reset_visitors),
          (set_visitor, 0, "trp_player"),
          (set_visitor, 1, "trp_npc11"),
          (set_visitor, 2, "trp_watchman"),
          (set_visitor, 3, "trp_farmer"),
          (set_visitor, 10, "trp_looter"),
          (set_visitor, 11, "trp_bandit"),
          (set_visitor, 12, "trp_henchman"),
          (set_jump_mission, "mt_companion_katrin_supply_watch"),
          (jump_to_scene, "scn_random_scene"),
          (change_screen_mission),
        ]
      ),
      ("katrin_watch_hide_shortage", [
          (main_party_has_troop, "trp_npc11"),
          (eq, "$g_sod_katrin_last_coin_pending", 1),
          (eq, "$g_sod_katrin_last_coin_witnessed", 1),
          (eq, "$g_sod_katrin_last_coin_confronted", 0),
        ], "Hide the shortage and keep morale bright for one more march.",
        [
          (assign, "$g_sod_katrin_last_coin_confronted", 1),
          (assign, "$g_sod_katrin_last_coin_result_grade", 1),
          (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_progress, 75),
          (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_metadata, "$g_sod_katrin_last_coin_result_grade"),
          (call_script, "script_sod_companion_shift_approval", "trp_npc11", -3),
          (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc11"),
          (display_message, "@The camp smiles for a day because it has not seen the numbers. Katrin has, and writes harder.", 0xCC9966),
          (start_map_conversation, "trp_npc11"),
        ]
      ),
      ("katrin_watch_leave", [], "Return to camp.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),

("katrin_supply_watch_succeeded", mnf_scale_picture|mnf_enable_hot_keys,
   "The store line holds. A few hungry fools learn that theft from a starving camp is not cleverness, and Katrin counts the sacks again before she counts bruises.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_katrin_last_coin_confronted", 1),
      (try_begin),
        (le, "$g_sod_katrin_last_coin_result_grade", 0),
        (assign, "$g_sod_katrin_last_coin_result_grade", 2),
      (try_end),
      (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_metadata, "$g_sod_katrin_last_coin_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc11"),
    ],
    [
      ("katrin_supply_watch_after", [], "Settle the last coin with Katrin.",
        [
          (start_map_conversation, "trp_npc11"),
        ]
      ),
    ]
  ),

("katrin_supply_watch_failed", mnf_scale_picture|mnf_enable_hot_keys,
   "The store line breaks before order returns. Nothing catastrophic is lost, but enough is spilled, stolen, or trampled that tomorrow has become thinner.",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_katrin_last_coin_confronted", 1),
      (assign, "$g_sod_katrin_last_coin_result_grade", -1),
      (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_progress, 75),
      (quest_set_slot, "qst_companion_katrin_last_coin", slot_quest_sod_runtime_metadata, "$g_sod_katrin_last_coin_result_grade"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc11"),
    ],
    [
      ("katrin_supply_watch_failed_after", [], "Face Katrin after the broken store line.",
        [
          (start_map_conversation, "trp_npc11"),
        ]
      ),
    ]
  ),
]
