MENUS = [
(
    "construct_ladders", mnf_enable_hot_keys,
    "{s68}",
    "none",
    [
      (set_background_mesh, "mesh_pic_construction"),

      (call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),
     (assign, reg2, ":max_skill"),

     #MORDACHAI - increase the effectiveness of engineering skill
     (store_sub, reg4, 12, ":max_skill"),
     (val_mul, reg4, 2),
     (val_div, reg4, 3),

     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
       (str_store_string, s68, "@As the party member with the highest Engineer skill ({reg2}), you estimate that it will take {reg4} hours to build enough scaling ladders for the assault."),
     (else_try),
       (assign, reg3, 0),
       (call_script, "script_store_troop_name", s3, ":max_skill_owner"),
       (str_store_string, s68, "@As the party member with the highest Engineer skill ({reg2}), {s3} estimates that it will take {reg4} hours to build enough scaling ladders for the assault."),
     (try_end),
    ],
    [
      ("build_ladders_artimenner_inspect", [
          (main_party_has_troop, "trp_npc15"),
          (eq, "$g_sod_artimenner_siege_pending", 1),
          (eq, "$g_sod_artimenner_siege_witnessed", 0),
          (troop_slot_eq, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ],
       "Have Artimenner inspect the ladder joints before work begins.", [
           (assign, "$g_sod_artimenner_siege_witnessed", 1),
           (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_progress, 50),
           (quest_set_slot, "qst_companion_artimenner_siege_that_should", slot_quest_sod_runtime_metadata, "$g_sod_artimenner_siege_result_grade"),
           (call_script, "script_sod_companion_apply_player_action", sod_companion_action_siege_preparation, 1),
           (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc15"),
           (display_message, "@Artimenner marks the weak ladder joints in chalk before the carpenters start cutting. The siege design now has a construction witness.", 0x99CCFF),
           (jump_to_menu, "mnu_construct_ladders"),
           ]),
      ("build_ladders_cont", [],
       "Do it.", [
           (assign, "$g_siege_method", 1),
           (store_current_hours, ":cur_hours"),
           (call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
           #MORDACHAI - increase the effectiveness of engineering skill
           (store_sub, ":hours_takes", 12, reg0),
           (val_mul, ":hours_takes", 2),
           (val_div, ":hours_takes", 3),
           (call_script, "script_sod_camp_apply_artimenner_siege_preparation_to_hours", ":hours_takes", 1),
           (assign, ":hours_takes", reg0),
           (store_add, "$g_siege_method_finish_hours", ":cur_hours", ":hours_takes"),
           (call_script, "script_sod_companion_apply_player_action", sod_companion_action_siege_preparation, 2),
           (call_script, "script_sod_companion_try_artimenner_siege_incident", 1, 2),
           (assign, "$auto_besiege_town", "$current_town"),
           (rest_for_hours_interactive, 96, 5, 1), #rest while attackable. A trigger will divert control when attack is ready.
           (change_screen_return),
           ]),
      ("go_back", [],
       "Go back.", [(jump_to_menu, "mnu_castle_besiege")]),
        ],
  ),
]
