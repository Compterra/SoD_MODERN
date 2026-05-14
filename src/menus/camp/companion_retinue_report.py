MENUS = [
("companion_retinue_report", mnf_scale_picture|mnf_enable_hot_keys,
   "{s1}",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (assign, "$g_sod_retinue_return_menu", "mnu_companion_retinue_report"),
      (call_script, "script_sod_companion_retinue_repair_all"),
      (call_script, "script_sod_companion_retinue_describe_report_to_s1"),
    ],
    [
      ("companion_retinue_global_post_battle_off", [
          (eq, "$g_sod_retinue_post_battle_hiring_disabled", 0),
        ], "Disable all post-battle retinue hiring.",
        [
          (assign, "$g_sod_retinue_post_battle_hiring_disabled", 1),
          (jump_to_menu, "mnu_companion_retinue_report"),
        ]
      ),
      ("companion_retinue_global_post_battle_on", [
          (gt, "$g_sod_retinue_post_battle_hiring_disabled", 0),
        ], "Enable post-battle retinue hiring.",
        [
          (assign, "$g_sod_retinue_post_battle_hiring_disabled", 0),
          (jump_to_menu, "mnu_companion_retinue_report"),
        ]
      ),
      ("companion_retinue_select_borcha", [(main_party_has_troop, "trp_npc1")], "Review Borcha's retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc1"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_select_marnid", [(main_party_has_troop, "trp_npc2")], "Review Marnid's retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc2"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_select_ymira", [(main_party_has_troop, "trp_npc3")], "Review Ymira's retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc3"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_select_rolf", [(main_party_has_troop, "trp_npc4")], "Review Rolf's retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc4"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_select_baheshtur", [(main_party_has_troop, "trp_npc5")], "Review Baheshtur's retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc5"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_select_firentis", [(main_party_has_troop, "trp_npc6")], "Review Firentis' retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc6"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_select_deshavi", [(main_party_has_troop, "trp_npc7")], "Review Deshavi's retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc7"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_select_matheld", [(main_party_has_troop, "trp_npc8")], "Review Matheld's retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc8"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_select_alayen", [(main_party_has_troop, "trp_npc9")], "Review Alayen's retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc9"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_select_bunduk", [(main_party_has_troop, "trp_npc10")], "Review Bunduk's retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc10"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_select_katrin", [(main_party_has_troop, "trp_npc11")], "Review Katrin's retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc11"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_select_jeremus", [(main_party_has_troop, "trp_npc12")], "Review Jeremus' retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc12"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_select_nizar", [(main_party_has_troop, "trp_npc13")], "Review Nizar's retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc13"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_select_lezalit", [(main_party_has_troop, "trp_npc14")], "Review Lezalit's retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc14"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_select_artimenner", [(main_party_has_troop, "trp_npc15")], "Review Artimenner's retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc15"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_select_klethi", [(main_party_has_troop, "trp_npc16")], "Review Klethi's retinue.",
        [(assign, "$g_sod_retinue_focus_companion", "trp_npc16"), (jump_to_menu, "mnu_companion_retinue_manage")]
      ),
      ("companion_retinue_report_back", [], "Return to camp actions.",
        [(jump_to_menu, "mnu_camp_action")]
      ),
    ]
  ),

("companion_retinue_manage", mnf_scale_picture|mnf_enable_hot_keys,
   "{s1}",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (call_script, "script_sod_companion_retinue_describe_focus_to_s1", "$g_sod_retinue_focus_companion"),
    ],
    [
      ("companion_retinue_order_none", [
          (is_between, "$g_sod_retinue_focus_companion", companions_begin, companions_end),
          (main_party_has_troop, "$g_sod_retinue_focus_companion"),
        ], "Stand this retinue down.",
        [
          (call_script, "script_sod_companion_retinue_set_strength_order", "$g_sod_retinue_focus_companion", sod_retinue_strength_none),
          (jump_to_menu, "mnu_companion_retinue_manage"),
        ]
      ),
      ("companion_retinue_order_half", [
          (is_between, "$g_sod_retinue_focus_companion", companions_begin, companions_end),
          (main_party_has_troop, "$g_sod_retinue_focus_companion"),
        ], "Keep this retinue at half strength.",
        [
          (call_script, "script_sod_companion_retinue_set_strength_order", "$g_sod_retinue_focus_companion", sod_retinue_strength_half),
          (jump_to_menu, "mnu_companion_retinue_manage"),
        ]
      ),
      ("companion_retinue_order_full", [
          (is_between, "$g_sod_retinue_focus_companion", companions_begin, companions_end),
          (main_party_has_troop, "$g_sod_retinue_focus_companion"),
        ], "Build this retinue to full strength.",
        [
          (call_script, "script_sod_companion_retinue_set_strength_order", "$g_sod_retinue_focus_companion", sod_retinue_strength_full),
          (jump_to_menu, "mnu_companion_retinue_manage"),
        ]
      ),
      ("companion_retinue_recruit_none", [
          (is_between, "$g_sod_retinue_focus_companion", companions_begin, companions_end),
          (main_party_has_troop, "$g_sod_retinue_focus_companion"),
        ], "Stop independent recruiting.",
        [
          (call_script, "script_sod_companion_retinue_set_recruit_policy", "$g_sod_retinue_focus_companion", sod_retinue_recruit_policy_none),
          (jump_to_menu, "mnu_companion_retinue_manage"),
        ]
      ),
      ("companion_retinue_recruit_cautious", [
          (is_between, "$g_sod_retinue_focus_companion", companions_begin, companions_end),
          (main_party_has_troop, "$g_sod_retinue_focus_companion"),
          (neg|troop_slot_eq, "$g_sod_retinue_focus_companion", slot_troop_sod_retinue_strength_order, sod_retinue_strength_none),
        ], "Recruit cautiously from spare purse funds.",
        [
          (call_script, "script_sod_companion_retinue_set_recruit_policy", "$g_sod_retinue_focus_companion", sod_retinue_recruit_policy_cautious),
          (jump_to_menu, "mnu_companion_retinue_manage"),
        ]
      ),
      ("companion_retinue_recruit_balanced", [
          (is_between, "$g_sod_retinue_focus_companion", companions_begin, companions_end),
          (main_party_has_troop, "$g_sod_retinue_focus_companion"),
          (neg|troop_slot_eq, "$g_sod_retinue_focus_companion", slot_troop_sod_retinue_strength_order, sod_retinue_strength_none),
        ], "Recruit steadily from spare purse funds.",
        [
          (call_script, "script_sod_companion_retinue_set_recruit_policy", "$g_sod_retinue_focus_companion", sod_retinue_recruit_policy_balanced),
          (jump_to_menu, "mnu_companion_retinue_manage"),
        ]
      ),
      ("companion_retinue_recruit_eager", [
          (is_between, "$g_sod_retinue_focus_companion", companions_begin, companions_end),
          (main_party_has_troop, "$g_sod_retinue_focus_companion"),
          (neg|troop_slot_eq, "$g_sod_retinue_focus_companion", slot_troop_sod_retinue_strength_order, sod_retinue_strength_none),
        ], "Recruit aggressively from spare purse funds.",
        [
          (call_script, "script_sod_companion_retinue_set_recruit_policy", "$g_sod_retinue_focus_companion", sod_retinue_recruit_policy_eager),
          (jump_to_menu, "mnu_companion_retinue_manage"),
        ]
      ),
      ("companion_retinue_post_battle_off", [
          (is_between, "$g_sod_retinue_focus_companion", companions_begin, companions_end),
          (main_party_has_troop, "$g_sod_retinue_focus_companion"),
          (neg|troop_slot_eq, "$g_sod_retinue_focus_companion", slot_troop_sod_retinue_post_battle_policy, sod_retinue_post_battle_disabled),
        ], "Do not take freed troops after battles.",
        [
          (call_script, "script_sod_companion_retinue_set_post_battle_policy", "$g_sod_retinue_focus_companion", sod_retinue_post_battle_disabled),
          (jump_to_menu, "mnu_companion_retinue_manage"),
        ]
      ),
      ("companion_retinue_post_battle_on", [
          (is_between, "$g_sod_retinue_focus_companion", companions_begin, companions_end),
          (main_party_has_troop, "$g_sod_retinue_focus_companion"),
          (troop_slot_eq, "$g_sod_retinue_focus_companion", slot_troop_sod_retinue_post_battle_policy, sod_retinue_post_battle_disabled),
        ], "Allow taking suitable freed troops after battles.",
        [
          (call_script, "script_sod_companion_retinue_set_post_battle_policy", "$g_sod_retinue_focus_companion", sod_retinue_post_battle_enabled),
          (jump_to_menu, "mnu_companion_retinue_manage"),
        ]
      ),
      ("companion_retinue_give_500", [
          (is_between, "$g_sod_retinue_focus_companion", companions_begin, companions_end),
          (main_party_has_troop, "$g_sod_retinue_focus_companion"),
          (store_troop_gold, ":gold", "trp_player"),
          (ge, ":gold", 500),
        ], "Give 500 denars to the command purse.",
        [
          (call_script, "script_sod_companion_retinue_add_gold", "$g_sod_retinue_focus_companion", 500),
          (jump_to_menu, "mnu_companion_retinue_manage"),
        ]
      ),
      ("companion_retinue_give_1000", [
          (is_between, "$g_sod_retinue_focus_companion", companions_begin, companions_end),
          (main_party_has_troop, "$g_sod_retinue_focus_companion"),
          (store_troop_gold, ":gold", "trp_player"),
          (ge, ":gold", 1000),
        ], "Give 1000 denars to the command purse.",
        [
          (call_script, "script_sod_companion_retinue_add_gold", "$g_sod_retinue_focus_companion", 1000),
          (jump_to_menu, "mnu_companion_retinue_manage"),
        ]
      ),
      ("companion_retinue_withdraw_500", [
          (is_between, "$g_sod_retinue_focus_companion", companions_begin, companions_end),
          (main_party_has_troop, "$g_sod_retinue_focus_companion"),
          (troop_slot_ge, "$g_sod_retinue_focus_companion", slot_troop_sod_retinue_treasury, 500),
        ], "Withdraw 500 unused denars.",
        [
          (call_script, "script_sod_companion_retinue_remove_gold", "$g_sod_retinue_focus_companion", 500),
          (jump_to_menu, "mnu_companion_retinue_manage"),
        ]
      ),
      ("companion_retinue_withdraw_all", [
          (is_between, "$g_sod_retinue_focus_companion", companions_begin, companions_end),
          (main_party_has_troop, "$g_sod_retinue_focus_companion"),
          (troop_slot_ge, "$g_sod_retinue_focus_companion", slot_troop_sod_retinue_treasury, 1),
        ], "Withdraw all unused command funds.",
        [
          (troop_get_slot, ":treasury", "$g_sod_retinue_focus_companion", slot_troop_sod_retinue_treasury),
          (call_script, "script_sod_companion_retinue_remove_gold", "$g_sod_retinue_focus_companion", ":treasury"),
          (jump_to_menu, "mnu_companion_retinue_manage"),
        ]
      ),
      ("companion_retinue_assign_troops", [
          (is_between, "$g_sod_retinue_focus_companion", companions_begin, companions_end),
          (main_party_has_troop, "$g_sod_retinue_focus_companion"),
          (call_script, "script_sod_companion_retinue_get_free_capacity", "$g_sod_retinue_focus_companion"),
          (gt, reg0, 0),
        ], "Place troops under this companion.",
        [
          (assign, "$g_sod_retinue_selected_troop", 0),
          (assign, "$g_sod_retinue_selected_count", 0),
          (jump_to_menu, "mnu_companion_retinue_assign_troops"),
        ]
      ),
      ("companion_retinue_reclaim_troops", [
          (is_between, "$g_sod_retinue_focus_companion", companions_begin, companions_end),
          (main_party_has_troop, "$g_sod_retinue_focus_companion"),
          (call_script, "script_sod_companion_retinue_get_size", "$g_sod_retinue_focus_companion"),
          (gt, reg0, 0),
        ], "Return troops to your command.",
        [
          (assign, "$g_sod_retinue_selected_troop", 0),
          (assign, "$g_sod_retinue_selected_count", 0),
          (jump_to_menu, "mnu_companion_retinue_reclaim_troops"),
        ]
      ),
      ("companion_retinue_manage_back", [], "Back.",
        [
          (try_begin),
            (gt, "$g_sod_retinue_return_menu", 0),
            (jump_to_menu, "$g_sod_retinue_return_menu"),
          (else_try),
            (change_screen_return),
          (try_end),
        ]
      ),
    ]
  ),

("companion_retinue_assign_troops", mnf_scale_picture|mnf_enable_hot_keys,
   "{s1}",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (call_script, "script_sod_companion_retinue_select_main_party_troop", "$g_sod_retinue_selected_troop", 0),
      (assign, "$g_sod_retinue_selected_troop", reg0),
      (assign, "$g_sod_retinue_selected_count", reg1),
      (call_script, "script_sod_companion_retinue_describe_transfer_to_s1", "$g_sod_retinue_focus_companion", 1, "$g_sod_retinue_selected_troop", "$g_sod_retinue_selected_count"),
    ],
    [
      ("companion_retinue_assign_next", [
          (gt, "$g_sod_retinue_selected_troop", 0),
        ], "Select the next troop stack.",
        [
          (call_script, "script_sod_companion_retinue_select_main_party_troop", "$g_sod_retinue_selected_troop", 1),
          (assign, "$g_sod_retinue_selected_troop", reg0),
          (assign, "$g_sod_retinue_selected_count", reg1),
          (jump_to_menu, "mnu_companion_retinue_assign_troops"),
        ]
      ),
      ("companion_retinue_assign_one", [
          (gt, "$g_sod_retinue_selected_troop", 0),
          (call_script, "script_sod_companion_retinue_can_accept_troop", "$g_sod_retinue_focus_companion", "$g_sod_retinue_selected_troop", 1),
          (eq, reg0, 1),
        ], "Assign one selected troop.",
        [
          (call_script, "script_sod_companion_retinue_add_troops", "$g_sod_retinue_focus_companion", "$g_sod_retinue_selected_troop", 1),
          (jump_to_menu, "mnu_companion_retinue_assign_troops"),
        ]
      ),
      ("companion_retinue_assign_five", [
          (gt, "$g_sod_retinue_selected_troop", 0),
          (call_script, "script_sod_companion_retinue_can_accept_troop", "$g_sod_retinue_focus_companion", "$g_sod_retinue_selected_troop", 5),
          (eq, reg0, 1),
        ], "Assign five selected troops.",
        [
          (call_script, "script_sod_companion_retinue_add_troops", "$g_sod_retinue_focus_companion", "$g_sod_retinue_selected_troop", 5),
          (jump_to_menu, "mnu_companion_retinue_assign_troops"),
        ]
      ),
      ("companion_retinue_assign_all_safe", [
          (gt, "$g_sod_retinue_selected_troop", 0),
          (call_script, "script_sod_companion_retinue_get_free_capacity", "$g_sod_retinue_focus_companion"),
          (gt, reg0, 0),
        ], "Assign as many as this companion can command.",
        [
          (call_script, "script_sod_companion_retinue_add_troops_up_to_capacity", "$g_sod_retinue_focus_companion", "$g_sod_retinue_selected_troop", "$g_sod_retinue_selected_count"),
          (jump_to_menu, "mnu_companion_retinue_assign_troops"),
        ]
      ),
      ("companion_retinue_assign_back", [], "Return to this retinue.",
        [(jump_to_menu, "mnu_companion_retinue_manage")]
      ),
    ]
  ),

("companion_retinue_reclaim_troops", mnf_scale_picture|mnf_enable_hot_keys,
   "{s1}",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (call_script, "script_sod_companion_retinue_select_retinue_troop", "$g_sod_retinue_focus_companion", "$g_sod_retinue_selected_troop", 0),
      (assign, "$g_sod_retinue_selected_troop", reg0),
      (assign, "$g_sod_retinue_selected_count", reg1),
      (call_script, "script_sod_companion_retinue_describe_transfer_to_s1", "$g_sod_retinue_focus_companion", 2, "$g_sod_retinue_selected_troop", "$g_sod_retinue_selected_count"),
    ],
    [
      ("companion_retinue_reclaim_next", [
          (gt, "$g_sod_retinue_selected_troop", 0),
        ], "Select the next troop stack.",
        [
          (call_script, "script_sod_companion_retinue_select_retinue_troop", "$g_sod_retinue_focus_companion", "$g_sod_retinue_selected_troop", 1),
          (assign, "$g_sod_retinue_selected_troop", reg0),
          (assign, "$g_sod_retinue_selected_count", reg1),
          (jump_to_menu, "mnu_companion_retinue_reclaim_troops"),
        ]
      ),
      ("companion_retinue_reclaim_one", [
          (gt, "$g_sod_retinue_selected_troop", 0),
          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
          (ge, ":free_capacity", 1),
        ], "Reclaim one selected troop.",
        [
          (call_script, "script_sod_companion_retinue_remove_troops", "$g_sod_retinue_focus_companion", "$g_sod_retinue_selected_troop", 1),
          (jump_to_menu, "mnu_companion_retinue_reclaim_troops"),
        ]
      ),
      ("companion_retinue_reclaim_five", [
          (gt, "$g_sod_retinue_selected_troop", 0),
          (ge, "$g_sod_retinue_selected_count", 5),
          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
          (ge, ":free_capacity", 5),
        ], "Reclaim five selected troops.",
        [
          (call_script, "script_sod_companion_retinue_remove_troops", "$g_sod_retinue_focus_companion", "$g_sod_retinue_selected_troop", 5),
          (jump_to_menu, "mnu_companion_retinue_reclaim_troops"),
        ]
      ),
      ("companion_retinue_reclaim_all_safe", [
          (gt, "$g_sod_retinue_selected_troop", 0),
          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
          (gt, ":free_capacity", 0),
        ], "Reclaim as many as your party can hold.",
        [
          (call_script, "script_sod_companion_retinue_remove_troops_up_to_capacity", "$g_sod_retinue_focus_companion", "$g_sod_retinue_selected_troop", "$g_sod_retinue_selected_count"),
          (jump_to_menu, "mnu_companion_retinue_reclaim_troops"),
        ]
      ),
      ("companion_retinue_reclaim_back", [], "Return to this retinue.",
        [(jump_to_menu, "mnu_companion_retinue_manage")]
      ),
    ]
  ),
]
