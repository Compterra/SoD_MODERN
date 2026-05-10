MENUS = [
(
    "seven_ash_ultimatum", mnf_disable_all_keys,
    "{s1}^^Rafe Carrick throws a sack at Reeve Martin's feet. Teeth, bent buckles, and three village tokens spill in the dirt.^^'Five thousand denars. Five hundred sacks of grain. Twelve children as surety. One hundred days. Refuse him and my uncle comes himself.'",
    "none",
    [
      (set_background_mesh, "mesh_pic_village_p"),
      (quest_get_slot, ":campaign_status", "qst_seven_ash_ultimatum", slot_quest_seven_ash_campaign_status),
      (try_begin),
        (eq, ":campaign_status", sod_seven_ash_status_inactive),
        (assign, "$g_sod_seven_ash_enabled", 1),
        (call_script, "script_sod_seven_ash_initialize_campaign_state"),
        (call_script, "script_party_count_fit_for_battle", "p_main_party", 0),
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_player_strength_ultimatum, reg0),
        (str_store_string, s1, "@Mother Hilda asks whether surety means hostage. Rafe smiles as if kindness were a word he can lend and take back. Reeve Martin looks at the granary keys. Piers Wainwright watches the road. Nell of Little Harrow watches the sack."),
      (else_try),
        (call_script, "script_sod_seven_ash_repair_campaign_state"),
        (str_store_string, s1, "@The ultimatum has already been answered. Ashwick's fear has moved from words into work, roads, and witnesses. Continue the current Seven Oaths stage instead of reopening Rafe's first demand."),
      (try_end),
    ],
    [
      ("seven_ash_prepare_alone", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_ultimatum),
      ], "Mother Hilda, we start with our own hands. Walls, grain, watches, carts.", [
        (call_script, "script_sod_seven_ash_choose_posture", sod_seven_ash_posture_prepare_alone),
        (jump_to_menu, "mnu_seven_ash_village_audit"),
      ]),
      ("seven_ash_find_defenders", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_ultimatum),
      ], "Nell, name anyone who has survived this kind of war. We ride for defenders.", [
        (call_script, "script_sod_seven_ash_choose_posture", sod_seven_ash_posture_find_defenders),
        (jump_to_menu, "mnu_seven_ash_village_audit"),
      ]),
      ("seven_ash_lordly_aid", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_ultimatum),
      ], "Reeve Martin, write to the nearest lord. Let law be forced to answer before ash does.", [
        (call_script, "script_sod_seven_ash_choose_posture", sod_seven_ash_posture_lordly_aid),
        (jump_to_menu, "mnu_seven_ash_village_audit"),
      ]),
      ("seven_ash_bargain", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_ultimatum),
      ], "Rafe, tell Wulfred I will hear terms before I spend children or steel.", [
        (call_script, "script_sod_seven_ash_choose_posture", sod_seven_ash_posture_bargain),
        (jump_to_menu, "mnu_seven_ash_village_audit"),
      ]),
      ("seven_ash_evacuate", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_ultimatum),
      ], "Piers, count carts and dry roads. If Ashwick cannot stand, its people will.", [
        (call_script, "script_sod_seven_ash_choose_posture", sod_seven_ash_posture_evacuate),
        (jump_to_menu, "mnu_seven_ash_village_audit"),
      ]),
      ("seven_ash_kill_messengers", [
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_ultimatum),
      ], "Rafe, no child leaves here as surety. Neither do you.", [
        (call_script, "script_sod_seven_ash_choose_posture", sod_seven_ash_posture_kill_messengers),
        (jump_to_menu, "mnu_seven_ash_village_audit"),
      ]),
      ("seven_ash_continue_current_stage", [
        (neg|quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_ultimatum),
      ], "Continue the Seven Oaths campaign.", [
        (quest_get_slot, ":stage", "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage),
        (try_begin),
          (eq, ":stage", sod_seven_ash_stage_audit),
          (jump_to_menu, "mnu_seven_ash_village_audit"),
        (else_try),
          (eq, ":stage", sod_seven_ash_stage_recruitment),
          (jump_to_menu, "mnu_seven_ash_recruitment_map"),
        (else_try),
          (eq, ":stage", sod_seven_ash_stage_return),
          (jump_to_menu, "mnu_seven_ash_return_to_ashwick"),
        (else_try),
          (eq, ":stage", sod_seven_ash_stage_pressure),
          (jump_to_menu, "mnu_seven_ash_pressure_board"),
        (else_try),
          (eq, ":stage", sod_seven_ash_stage_oath_council),
          (jump_to_menu, "mnu_seven_ash_oath_council"),
        (else_try),
          (eq, ":stage", sod_seven_ash_stage_siege),
          (jump_to_menu, "mnu_seven_ash_siege_warning"),
        (else_try),
          (eq, ":stage", sod_seven_ash_stage_aftermath),
          (jump_to_menu, "mnu_seven_ash_aftermath_staging"),
        (else_try),
          (jump_to_menu, "mnu_start_phase_2"),
        (try_end),
      ]),
      ("seven_ash_not_now", [], "Leave Ashwick for now.", [
        (jump_to_menu, "mnu_start_phase_2"),
      ]),
    ]
  ),
]

