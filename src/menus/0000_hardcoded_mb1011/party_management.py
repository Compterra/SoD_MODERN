MENUS = [
("party_management", mnf_scale_picture|mnf_enable_hot_keys,
   "What do you want to do?",
   "none",
   [
     (assign, "$g_player_icon_state", pis_normal),
     (set_background_mesh, "mesh_pic_camp"),
    ],
    [

		# Jedediah Q's Companion Overview
      ("Companions_overview",
        [(call_script, "script_get_count_of_companions"), (gt, reg0, 0)],
        "Companions overview.",
        [
          (assign, "$jq_in_market_menu", 0), # player is not in market menu
          (start_presentation, "prsnt_jq_companions_quickview"),
       ]
      ),

      # Autoloot: Allow item management from camp
      ("camp_manage_inventory",
        [(call_script, "script_get_count_of_companions"), (gt, reg0, 0)],
        "Party's inventory.",
        [
          (troop_clear_inventory, "trp_temp_troop"),
          (assign, "$return_menu", "mnu_camp"),
          (assign, "$inventory_menu_offset", 0),
          (str_clear, s30),
          (jump_to_menu, "mnu_manage_loot_pool")
        ]
      ),
	  
      ("camp_promote", [], "Promote mercenaries.", [(jump_to_menu, "mnu_sod_upgrade_camp")]),

      ("camp_recruit_prisoners",
        [
          (troops_can_join, 1),
          (store_current_hours, ":cur_time"),
          (val_sub, ":cur_time", 24),
          (gt, ":cur_time", "$g_prisoner_recruit_last_time"),
          (try_begin),
            (gt, "$g_prisoner_recruit_last_time", 0),
            (assign, "$g_prisoner_recruit_troop_id", 0),
            (assign, "$g_prisoner_recruit_size", 0),
            (assign, "$g_prisoner_recruit_last_time", 0),
          (try_end),

          # don't allow this option if they haven't any prisoners.. a'duh!
          (assign, ":num_regular_prisoner_slots", 0),
          (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
          (try_for_range, ":cur_stack", 0, ":num_stacks"),
            (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":cur_stack"),
            (neg|troop_is_hero, ":cur_troop_id"),
            (is_between, ":cur_troop_id", soldiers_begin, soldiers_end),
            (val_add, ":num_regular_prisoner_slots", 1),
          (try_end),
          (neq, ":num_regular_prisoner_slots", 0),
        ],
        "Recruit prisoners.",
        [
          (jump_to_menu, "mnu_camp_recruit_prisoners"),
        ],
      ),
	
      ("resume_travelling", [], "Back.", [(jump_to_menu, "mnu_camp"), ]),
	  
	 ]),
]
