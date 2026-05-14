MENUS = [
("camp_action", mnf_scale_picture|mnf_enable_hot_keys,
   "Choose an action:",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
    ],
    [
      ("camp_company_accounts", [], "Settle company accounts.",
        [
          (jump_to_menu, "mnu_company_accounts"),
        ]
      ),

      ("camp_company_rations", [], "Set ration policy.",
        [
          (jump_to_menu, "mnu_company_rations"),
        ]
      ),

      ("camp_company_recreation", [], "Arrange company relief.",
        [
          (jump_to_menu, "mnu_company_recreation"),
        ]
      ),

      ("camp_disable_player_tax_couriers", [
          (eq, "$g_sod_player_tax_couriers_enabled", 1),
        ], "Disable tax couriers for your fiefs.",
        [
          (assign, "$g_sod_player_tax_couriers_enabled", 0),
          (display_message, "@Your stewards will hold tax income at each fief until you collect it directly.", 0x99CCFF),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),

      ("camp_enable_player_tax_couriers", [
          (neq, "$g_sod_player_tax_couriers_enabled", 1),
        ], "Enable tax couriers for your fiefs.",
        [
          (assign, "$g_sod_player_tax_couriers_enabled", 1),
          (display_message, "@Your stewards will dispatch tax couriers from eligible fiefs.", 0x99CCFF),
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),

      ("camp_action_read_book", [], "Choose a book for the road.",
        [
          (jump_to_menu, "mnu_camp_action_read_book"),
        ]
      ),

      ("camp_jobs", [], "Manage camp jobs and expedition roles.",
        [
          (jump_to_menu, "mnu_camp_jobs"),
        ]
      ),

      ("camp_strategy_advisor",
        [(main_party_has_troop, "trp_sod_strategy_advisor"),
        ],
        "Speak with Cassian Varro.",
        [
          (assign, "$sa_talk_after_siege", 0),
          (start_map_conversation, "trp_sod_strategy_advisor"),
          (change_screen_return),
        ]
      ),

      ("camp_quick_start", [], "Quick start.",
        [
          (jump_to_menu, "mnu_quick_start"),
        ]
      ),

      ("camp_retire", [], "Retire from adventuring.",
        [
          (jump_to_menu, "mnu_retirement_verify"),
        ]
      ),

      ("camp_free_slaves", [
          (party_count_members_of_type, ":male_slaves", "p_main_party", "trp_slave"),
          (party_count_members_of_type, ":female_slaves", "p_main_party", "trp_slave_female"),
          (store_add, ":slave_count", ":male_slaves", ":female_slaves"),
          (gt, ":slave_count", 0),
        ], "Free slaves from your party.",
        [
          (jump_to_menu, "mnu_free_slaves_confirm"),
        ]
      ),

      ("camp_ymira_mercy_under_arms", [
          (main_party_has_troop, "trp_npc3"),
          (this_or_next|troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
          (troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
          (party_count_members_of_type, ":male_slaves", "p_main_party", "trp_slave"),
          (party_count_members_of_type, ":female_slaves", "p_main_party", "trp_slave_female"),
          (store_add, ":slave_count", ":male_slaves", ":female_slaves"),
          (ge, ":slave_count", 3),
        ], "Speak with Ymira about the captives.",
        [
          (jump_to_menu, "mnu_ymira_mercy_under_arms"),
        ]
      ),
      ("camp_borcha_road_keeps_own", [
          (main_party_has_troop, "trp_npc1"),
          (eq, "$g_sod_borcha_road_pending", 1),
          (troop_slot_eq, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Speak with Borcha about the hidden road.",
        [
          (jump_to_menu, "mnu_borcha_road_keeps_own"),
        ]
      ),
      ("camp_marnid_honest_price", [
          (main_party_has_troop, "trp_npc2"),
          (eq, "$g_sod_marnid_market_pending", 1),
          (troop_slot_eq, "trp_npc2", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Speak with Marnid about the suspect contract.",
        [
          (jump_to_menu, "mnu_marnid_honest_price"),
        ]
      ),

      ("camp_lezalit_discipline_without_chains", [
          (main_party_has_troop, "trp_npc14"),
          (eq, "$g_sod_lezalit_ief_discipline_pending", 1),
          (eq, "$g_sod_lezalit_ief_discipline_confronted", 1),
          (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Speak with Lezalit about the captured Imperial drill.",
        [
          (jump_to_menu, "mnu_lezalit_discipline_without_chains"),
        ]
      ),
      ("camp_lezalit_drill_trial", [
          (main_party_has_troop, "trp_npc14"),
          (eq, "$g_sod_lezalit_ief_discipline_pending", 1),
          (eq, "$g_sod_lezalit_ief_discipline_witnessed", 1),
          (eq, "$g_sod_lezalit_ief_discipline_confronted", 0),
          (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Run Lezalit's captured drill trial.",
        [
          (jump_to_menu, "mnu_lezalit_drill_trial"),
        ]
      ),

      ("camp_bunduk_men_hold_line", [
          (main_party_has_troop, "trp_npc10"),
          (eq, "$g_sod_bunduk_line_pending", 1),
          (troop_slot_eq, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Speak with Bunduk about the line's grievance.",
        [
          (jump_to_menu, "mnu_bunduk_men_hold_line"),
        ]
      ),
      ("camp_bunduk_line_test", [
          (main_party_has_troop, "trp_npc10"),
          (eq, "$g_sod_bunduk_line_pending", 1),
          (eq, "$g_sod_bunduk_line_witnessed", 1),
          (eq, "$g_sod_bunduk_line_confronted", 0),
          (troop_slot_eq, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Run Bunduk's watch-line test.",
        [
          (jump_to_menu, "mnu_bunduk_line_test"),
        ]
      ),

      ("camp_jeremus_hands_triage", [
          (main_party_has_troop, "trp_npc12"),
          (eq, "$g_sod_jeremus_triage_pending", 1),
          (eq, "$g_sod_jeremus_triage_confronted", 1),
          (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Speak with Jeremus among the wounded.",
        [
          (jump_to_menu, "mnu_jeremus_hands_triage"),
        ]
      ),
      ("camp_jeremus_infirmary_crisis", [
          (main_party_has_troop, "trp_npc12"),
          (eq, "$g_sod_jeremus_triage_pending", 1),
          (eq, "$g_sod_jeremus_triage_witnessed", 1),
          (eq, "$g_sod_jeremus_triage_confronted", 0),
          (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Face Jeremus' infirmary crisis.",
        [
          (jump_to_menu, "mnu_jeremus_triage_infirmary"),
        ]
      ),

      ("camp_firentis_debt_restitution", [
          (main_party_has_troop, "trp_npc6"),
          (eq, "$g_sod_firentis_restitution_pending", 1),
          (troop_slot_eq, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Speak with Firentis about restitution.",
        [
          (jump_to_menu, "mnu_firentis_debt_restitution"),
        ]
      ),

      ("camp_katrin_last_coin", [
          (main_party_has_troop, "trp_npc11"),
          (eq, "$g_sod_katrin_last_coin_pending", 1),
          (eq, "$g_sod_katrin_last_coin_confronted", 1),
          (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Speak with Katrin about the last coin.",
        [
          (jump_to_menu, "mnu_katrin_last_coin"),
        ]
      ),
      ("camp_katrin_supply_watch", [
          (main_party_has_troop, "trp_npc11"),
          (eq, "$g_sod_katrin_last_coin_pending", 1),
          (eq, "$g_sod_katrin_last_coin_witnessed", 1),
          (eq, "$g_sod_katrin_last_coin_confronted", 0),
          (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Run Katrin's supply watch.",
        [
          (jump_to_menu, "mnu_katrin_supply_watch"),
        ]
      ),

      ("camp_deshavi_tracks_through_ash", [
          (main_party_has_troop, "trp_npc7"),
          (eq, "$g_sod_deshavi_trail_warning_pending", 1),
          (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Speak with Deshavi about the trail warning.",
        [
          (jump_to_menu, "mnu_deshavi_tracks_through_ash"),
        ]
      ),

      ("camp_klethi_knife_with_name", [
          (main_party_has_troop, "trp_npc16"),
          (eq, "$g_sod_klethi_old_job_pending", 1),
          (troop_slot_eq, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Speak with Klethi about the old job.",
        [
          (jump_to_menu, "mnu_klethi_knife_with_name"),
        ]
      ),

      ("camp_rolf_name_worth_wearing", [
          (main_party_has_troop, "trp_npc4"),
          (eq, "$g_sod_rolf_name_challenge_pending", 1),
          (eq, "$g_sod_rolf_name_challenge_confronted", 1),
          (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Speak with Rolf about the public challenge.",
        [
          (jump_to_menu, "mnu_rolf_name_worth_wearing"),
        ]
      ),
      ("camp_rolf_public_proof", [
          (main_party_has_troop, "trp_npc4"),
          (eq, "$g_sod_rolf_name_challenge_pending", 1),
          (eq, "$g_sod_rolf_name_challenge_witnessed", 1),
          (eq, "$g_sod_rolf_name_challenge_confronted", 0),
          (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Stage Rolf's public proof.",
        [
          (jump_to_menu, "mnu_rolf_public_proof"),
        ]
      ),

      ("camp_alayen_standard_self", [
          (main_party_has_troop, "trp_npc9"),
          (eq, "$g_sod_alayen_standard_pending", 1),
          (eq, "$g_sod_alayen_standard_confronted", 1),
          (troop_slot_eq, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Speak with Alayen about the standard oath.",
        [
          (jump_to_menu, "mnu_alayen_standard_self"),
        ]
      ),
      ("camp_alayen_standard_test", [
          (main_party_has_troop, "trp_npc9"),
          (eq, "$g_sod_alayen_standard_pending", 1),
          (eq, "$g_sod_alayen_standard_witnessed", 1),
          (eq, "$g_sod_alayen_standard_confronted", 0),
          (troop_slot_eq, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Stand Alayen's public standard test.",
        [
          (jump_to_menu, "mnu_alayen_standard_test"),
        ]
      ),

      ("camp_nizar_impossible_charge", [
          (main_party_has_troop, "trp_npc13"),
          (eq, "$g_sod_nizar_charge_pending", 1),
          (eq, "$g_sod_nizar_charge_confronted", 1),
          (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Speak with Nizar about the impossible charge.",
        [
          (jump_to_menu, "mnu_nizar_impossible_charge"),
        ]
      ),
      ("camp_nizar_charge_lane_test", [
          (main_party_has_troop, "trp_npc13"),
          (eq, "$g_sod_nizar_charge_pending", 1),
          (eq, "$g_sod_nizar_charge_witnessed", 1),
          (eq, "$g_sod_nizar_charge_confronted", 0),
          (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Run Nizar's charge-lane test.",
        [
          (jump_to_menu, "mnu_nizar_charge_lane_test"),
        ]
      ),

      ("camp_baheshtur_unbroken_saddle", [
          (main_party_has_troop, "trp_npc5"),
          (eq, "$g_sod_baheshtur_saddle_pending", 1),
          (eq, "$g_sod_baheshtur_saddle_confronted", 1),
          (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Speak with Baheshtur about the saddle oath.",
        [
          (jump_to_menu, "mnu_baheshtur_unbroken_saddle"),
        ]
      ),
      ("camp_baheshtur_rider_oath_trial", [
          (main_party_has_troop, "trp_npc5"),
          (eq, "$g_sod_baheshtur_saddle_pending", 1),
          (eq, "$g_sod_baheshtur_saddle_witnessed", 1),
          (eq, "$g_sod_baheshtur_saddle_confronted", 0),
          (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Run Baheshtur's rider-oath trial.",
        [
          (jump_to_menu, "mnu_baheshtur_rider_oath_trial"),
        ]
      ),

      ("camp_matheld_no_backward_step", [
          (main_party_has_troop, "trp_npc8"),
          (eq, "$g_sod_matheld_no_backward_step_pending", 1),
          (eq, "$g_sod_matheld_no_backward_step_confronted", 1),
          (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Speak with Matheld about the shield challenge.",
        [
          (jump_to_menu, "mnu_matheld_no_backward_step"),
        ]
      ),
      ("camp_matheld_shield_line_test", [
          (main_party_has_troop, "trp_npc8"),
          (eq, "$g_sod_matheld_no_backward_step_pending", 1),
          (eq, "$g_sod_matheld_no_backward_step_witnessed", 1),
          (eq, "$g_sod_matheld_no_backward_step_confronted", 0),
          (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Run Matheld's shield-line test.",
        [
          (jump_to_menu, "mnu_matheld_shield_line_test"),
        ]
      ),

      ("camp_artimenner_siege_that_should", [
          (main_party_has_troop, "trp_npc15"),
          (eq, "$g_sod_artimenner_siege_pending", 1),
          (eq, "$g_sod_artimenner_siege_confronted", 1),
          (troop_slot_eq, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Speak with Artimenner about the siege design.",
        [
          (jump_to_menu, "mnu_artimenner_siege_that_should"),
        ]
      ),
      ("camp_artimenner_repair_watch", [
          (main_party_has_troop, "trp_npc15"),
          (eq, "$g_sod_artimenner_siege_pending", 1),
          (eq, "$g_sod_artimenner_siege_witnessed", 1),
          (eq, "$g_sod_artimenner_siege_confronted", 0),
          (troop_slot_eq, "trp_npc15", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
        ], "Guard Artimenner's repair watch.",
        [
          (jump_to_menu, "mnu_artimenner_repair_watch"),
        ]
      ),

      ("camp_companion_campfire", [
          (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
          (gt, ":num_stacks", 1),
        ], "Gather your companions by the fire.",
        [
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),

      ("camp_companion_depth_report", [
          (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
          (gt, ":num_stacks", 1),
        ], "Review companion depth report.",
        [
          (jump_to_menu, "mnu_companion_depth_report"),
        ]
      ),

      ("camp_companion_retinue_report", [
          (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
          (gt, ":num_stacks", 1),
        ], "Review companion retinues.",
        [
          (jump_to_menu, "mnu_companion_retinue_report"),
        ]
      ),

      ("camp_companion_depth_debug", [
          (eq, "$g_sod_debug", 1),
        ], "DEBUG: Inspect companion approval bands.",
        [
          (jump_to_menu, "mnu_companion_depth_report"),
        ]
      ),

      ("camp_companion_interactive_quest_qa", [
          (eq, "$g_sod_debug", 1),
        ], "DEBUG: Companion interactive quest QA.",
        [
          (jump_to_menu, "mnu_companion_interactive_quest_qa"),
        ]
      ),

### NEW: attempt to replace every regular in the game with new instances to update their stats ###
### FAILS: you must start a new game to get new troop stats ###
      ("fix_regulars", [(eq, "$g_sod_debug", 1), (eq, 1, 0)], "DEBUG: Replace all troops from prototypes [DANGEROUS].",
        [
          # generate the count of instances
          (try_for_parties, ":party"),

            (str_store_party_name_link, s1, ":party"),
            (display_message, "@Refreshing {s1}", powder_blue),

            # iterate over all the members in each party
            (assign, ":index", 0),
            (party_get_num_companion_stacks, ":num_stacks", ":party"),
            (try_for_range, ":unused", 1, ":num_stacks"),
              # get the troop ID
              (party_stack_get_troop_id, ":troop", ":party", ":index"),
              # only regular troops (not characters)
              (try_begin),
                # skip over any heros in the party (this does cause their order to change... but that's tough to avoid (unless we use a temp party & swap)
                (troop_is_hero, ":troop"),
                (val_add, ":index", 1),
              (else_try),
                # replace the entire stack with a newly minted one (at the end of the party)
                (party_stack_get_size, ":count", ":party", ":index"),
                (party_remove_members, ":party", ":troop", ":count"),
                (party_add_members, ":party", ":troop", ":count"),
              (try_end),
            (try_end),

            # iterate over all the prisoner stacks in each party
            (assign, ":index", 0),
            (party_get_num_prisoner_stacks, ":num_stacks", ":party"),
            (try_for_range, ":unused", 1, ":num_stacks"),
              # get the troop ID
              (party_prisoner_stack_get_troop_id, ":troop", ":party", ":index"),
              # only regular troops (not characters)
              (try_begin),
                # skip over any heros in the party (this does cause their order to change... but that's tough to avoid (unless we use a temp party & swap)
                (troop_is_hero, ":troop"),
                (val_add, ":index", 1),
              (else_try),
                # replace the entire stack with a newly minted one (at the end of the party)
                (party_prisoner_stack_get_size, ":count", ":party", ":index"),
                (party_remove_prisoners, ":party", ":troop", ":count"),
                (party_add_prisoners, ":party", ":troop", ":count"),
              (try_end),
            (try_end),

          (try_end),
        ]
      ),

      ("fix_dups", [(eq, "$g_sod_debug", 1), (eq, "$g_fix_dup_troops", 0)], "DEBUG: Remove duplicate lords!",
        [
          (display_message, "@FINDING & FIXING DUPLICATE LORDS...", debug_color),

          # generate the count of instances
          (try_for_parties, ":party"),
            (neg|is_between, ":party", "p_temp_party", "p_town_merc_1"), # don't consider temp parties (they have duplicates by definition)
            (party_get_num_companion_stacks, ":num_stacks", ":party"),
            (try_for_range, ":i_stack", 0, ":num_stacks"),
              (party_stack_get_troop_id, ":troop", ":party", ":i_stack"),
              (troop_is_hero, ":troop"), # only heros - regulars aren't unique
              (troop_get_slot, ":count", ":troop", troop_slot_instances),
              (val_add, ":count", 1),
              (troop_set_slot, ":troop", troop_slot_instances, ":count"),
            (try_end),
          (try_end),

          # keep track of count of fixed troops
          (assign, ":fixed", 0),

          # for each duplicated hero, delete occurrences where they're not the leader of that party
          (try_for_parties, ":party"),
            (neg|is_between, ":party", "p_temp_party", "p_town_merc_1"), # don't consider temp parties (they have duplicates by definition)
            (party_get_num_companion_stacks, ":num_stacks", ":party"),
            (try_for_range, ":i_stack", 1, ":num_stacks"),
              (party_stack_get_troop_id, ":troop", ":party", ":i_stack"),
              (troop_is_hero, ":troop"),
              (try_begin),
                (troop_slot_ge, ":troop", troop_slot_instances, 2),

                # kill this duplicate copy!
                (party_stack_get_size, ":count", ":party", ":i_stack"),
                (party_remove_members, ":party", ":troop", ":count"),

                # document the change
                (assign, reg1, ":count"),
                (store_sub, reg0, ":count", 1),
                (str_store_troop_name_by_count, s1, ":troop", ":count"),
                (str_store_party_name, s2, ":party"),
                (try_begin),
                  (gt, ":count", 1),
                  (display_message, "@{reg1} {s1} in {s2} ...deleted", red),
                (else_try),
                  (display_message, "@{s1} in {s2} ...deleted", red),
                (try_end),
                (val_add, ":fixed", 1),

                # adjust indexes for removing this stack
                (val_sub, ":i_stack", 1), #NOTE: this doesn't really work... only the end can be modified, not the index variable
                (val_sub, ":num_stacks", 1),

                # adjust the count of instances of this hero
                (troop_get_slot, ":instances", ":troop", troop_slot_instances),
                (val_sub, ":instances", 1),
                (troop_set_slot, ":troop", troop_slot_instances, ":instances"),

              (try_end),
            (try_end),
          (try_end),

          # reset the counts
          (try_for_parties, ":party"),
            (party_get_num_companion_stacks, ":num_stacks", ":party"),
            (neg|is_between, ":party", "p_temp_party", "p_town_merc_1"), # don't consider temp parties (they have duplicates by definition)
            (try_for_range, ":i_stack", 0, ":num_stacks"),
              (party_stack_get_troop_id, ":troop", ":party", ":i_stack"),
              (troop_is_hero, ":troop"),
              (troop_set_slot, ":troop", troop_slot_instances, 0),
            (try_end),
          (try_end),

          # report analysis
          (assign, reg0, ":fixed"),
          (try_begin),
            (eq, reg0, 0),
            (display_message, "@No duplicates found! :)", green),
            (assign, "$g_fix_dup_troops", 1),
          (else_try),
            (display_message, "@Fixed {reg0} duplicates", debug_color),
          (try_end),
        ]
      ),

      ("camp_action_4", [], "Back to camp menu.",
        [
          (jump_to_menu, "mnu_camp"),
        ]
      ),
    ]
  ),
]
