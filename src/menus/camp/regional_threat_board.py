MENUS = [
("regional_threat_board", mnf_enable_hot_keys,
    "{s1}",
    "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),
      (try_begin),
        (check_quest_active, "qst_regional_threat_contract"),
        (call_script, "script_sod_threat_board_describe_active_contract"),
      (else_try),
        (try_begin),
          (le, "$g_sod_threat_board_context_center", 0),
          (call_script, "script_get_closest_center", "p_main_party"),
          (assign, "$g_sod_threat_board_context_center", reg0),
        (try_end),
        (call_script, "script_sod_threat_board_generate_offers", "$g_sod_threat_board_context_center"),
        (str_store_party_name, s2, "$g_sod_threat_board_context_center"),
        (str_store_string, s1, "@Regional Threat Board - {s2}^^Three notices are posted for captains willing to do hard, useful work. Each contract spawns or marks a real warband, pays once, and carries a deadline.^^Choose a contract:"),
      (try_end),
    ],
    [
      ("claim_completed_threat", [
          (check_quest_active, "qst_regional_threat_contract"),
          (quest_slot_eq, "qst_regional_threat_contract", slot_quest_sod_threat_ready_to_claim, 1),
        ], "Claim the posted reward.",
        [
          (call_script, "script_sod_threat_board_complete_contract"),
          (jump_to_menu, "mnu_regional_threat_board"),
        ]),

      ("view_active_threat", [
          (check_quest_active, "qst_regional_threat_contract"),
          (neg|quest_slot_eq, "qst_regional_threat_contract", slot_quest_sod_threat_ready_to_claim, 1),
        ], "Review the active contract.",
        [
          (display_message, "@The marked warband remains at large. Track it down before the deadline.", 0xFFCC66),
          (jump_to_menu, "mnu_regional_threat_board"),
        ]),

      ("abandon_active_threat", [
          (check_quest_active, "qst_regional_threat_contract"),
          (neg|quest_slot_eq, "qst_regional_threat_contract", slot_quest_sod_threat_ready_to_claim, 1),
        ], "Abandon the active contract.",
        [
          (quest_get_slot, ":sponsor_center", "qst_regional_threat_contract", slot_quest_sod_threat_sponsor_center),
          (call_script, "script_change_player_relation_with_center", ":sponsor_center", -1),
          (call_script, "script_sod_threat_board_fail_contract"),
          (jump_to_menu, "mnu_regional_threat_board"),
        ]),

      ("accept_threat_1", [
          (neg|check_quest_active, "qst_regional_threat_contract"),
          (call_script, "script_sod_threat_board_describe_offer", 1),
        ], "{s1}",
        [
          (call_script, "script_sod_threat_board_accept_contract", 1),
          (jump_to_menu, "mnu_regional_threat_board"),
        ]),

      ("accept_threat_2", [
          (neg|check_quest_active, "qst_regional_threat_contract"),
          (call_script, "script_sod_threat_board_describe_offer", 2),
        ], "{s1}",
        [
          (call_script, "script_sod_threat_board_accept_contract", 2),
          (jump_to_menu, "mnu_regional_threat_board"),
        ]),

      ("accept_threat_3", [
          (neg|check_quest_active, "qst_regional_threat_contract"),
          (call_script, "script_sod_threat_board_describe_offer", 3),
        ], "{s1}",
        [
          (call_script, "script_sod_threat_board_accept_contract", 3),
          (jump_to_menu, "mnu_regional_threat_board"),
        ]),

      ("threat_board_back", [], "Back.",
        [
          (try_begin),
            (gt, "$g_sod_threat_board_return_menu", 0),
            (jump_to_menu, "$g_sod_threat_board_return_menu"),
          (else_try),
            (jump_to_menu, "mnu_reports"),
          (try_end),
        ]),
    ]
  ),
]
