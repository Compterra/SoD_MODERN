MENUS = [
("manage_loot_pool", mnf_scale_picture|mnf_enable_hot_keys,
        "{s10}^{s30}",
        "none",
      [
        (set_background_mesh, "mesh_pic_camp"),

        # ensure that the autoloot data is correct for this version of autoloot
        (call_script, "script_init_auto_loot", 0),

        (assign, "$pool_troop", "trp_temp_troop"),
        (assign, reg20, 0),
        (troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
        (try_for_range, ":i_slot", 0, ":inv_cap"),
          (troop_get_inventory_slot, ":item_id", "$pool_troop", ":i_slot"),
          (ge, ":item_id", 0),
          (val_add, reg20, 1),
        (try_end),
        # reg20 now contains number of items in loot pool
        (try_begin),
          (eq, reg20, 0),
          (str_store_string, 10, "str_item_pool_no_items"),
          (str_store_string, 20, "str_item_pool_leave"),
        (else_try),
          (eq, reg20, 1),
          (str_store_string, 10, "str_item_pool_one_item"),
          (str_store_string, 20, "str_item_pool_abandon"),
        (else_try),
          (str_store_string, 10, "str_item_pool_many_items"),
          (str_store_string, 20, "str_item_pool_abandon"),
        (try_end),
        (assign, reg10, 0),
        (assign, reg11, 0),
        (assign, reg12, 0),
        (assign, reg13, 0),
        (assign, reg14, 0),
        (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
        (try_for_range, ":i_stack", 1, ":num_stacks"),
          (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
          (is_between, ":stack_troop", companions_begin, companions_end),
          (val_add, reg10, 1),
            (try_begin),
                (store_add, reg2, "$inventory_menu_offset", 1),
                (eq, reg10, reg2),
                (assign, reg11, ":stack_troop"),
                (call_script, "script_store_troop_name", 11, ":stack_troop"),
            (else_try),
                (store_add, reg2, "$inventory_menu_offset", 2),
                (eq, reg10, reg2),
                (assign, reg12, ":stack_troop"),
                (call_script, "script_store_troop_name", 12, ":stack_troop"),
            (else_try),
                (store_add, reg2, "$inventory_menu_offset", 3),
                (eq, reg10, reg2),
                (assign, reg13, ":stack_troop"),
                (call_script, "script_store_troop_name", 13, ":stack_troop"),
            (else_try),
                (store_add, reg2, "$inventory_menu_offset", 4),
                (eq, reg10, reg2),
                (assign, reg14, ":stack_troop"),
                (call_script, "script_store_troop_name", 14, ":stack_troop"),
            (try_end),
          (try_end),
          # reg10 now contains total num of heroes
        ],
        [
            ("auto_no_companions", [(eq, reg10, 0), (disable_menu_option)], "I have no companions to give loot to, yet", []),
            ("auto_loot",
                [
                    (gt, reg10, 0), # show this only if you have companions
                    (eq, "$inventory_menu_offset", 0),
                    (store_free_inventory_capacity, ":space", "$pool_troop"),
                    (ge, ":space", 10),
                    (try_begin),
                      (eq, reg20, 0), # disable if nothing to give out
                      (disable_menu_option),
                    (try_end),
                ],
                "Let your heroes select gear from the item pool.",
                [
                    #MORDACHAI - just do it - no confirmation
                    (call_script, "script_auto_loot_all"),
                    (jump_to_menu, "mnu_manage_loot_pool")
                ]
            ),
            ("auto_loot_no",
                [
                    (gt, reg10, 0), # show this only if you have companions
                    (gt, reg20, 0), # show this only if there are items to loot
                    (eq, "$inventory_menu_offset", 0),
                    (store_free_inventory_capacity, ":space", "$pool_troop"),
                    (lt, ":space", 10),
                    (disable_menu_option)
                ],
                "Insufficient item pool space for auto-upgrade.",
                []
            ),
            ("prev",
                [
                    (gt, reg10, 0), # show only if you have companions
                    (neq, "$inventory_menu_offset", 0)
                ],
                "[Previous page]",
                [
                    (val_sub, "$inventory_menu_offset", num_loot_management_menu_heroes),
                    (jump_to_menu, "mnu_manage_loot_pool")
                ]
            ),
            ("loot",
                [],
                "Access the item pool.",
                [
                    (change_screen_loot, "$pool_troop")
                ]
            ),
            ("companion1",
                [
                    (gt, reg11, 0)
                ],
                "Talk to {s11}",
                [
                    (assign, "$g_camp_talk", 1),
                    (call_script, "script_setup_troop_meeting", reg11, 0)
                ]
            ),
            ("companion2",
                [
                    (gt, reg12, 0)
                ],
                "Talk to {s12}",
                [
                    (assign, "$g_camp_talk", 1),
                    (call_script, "script_setup_troop_meeting", reg12, 0)
                ]
            ),
            ("companion3",
                [
                    (gt, reg13, 0)
                ],
                "Talk to {s13}",
                [
                    (assign, "$g_camp_talk", 1),
                    (call_script, "script_setup_troop_meeting", reg13, 0)
                ]
            ),
            ("companion4",
                [
                    (gt, reg14, 0)
                ],
                "Talk to {s14}",
                [
                    (assign, "$g_camp_talk", 1),
                    (call_script, "script_setup_troop_meeting", reg14, 0)
                ]
            ),
            ("next",
                [
                    (gt, reg10, 0), # show only if you have companions
                    (try_begin),
                        (le, reg10, num_loot_management_menu_heroes), #enough entries for everyone
                        (disable_menu_option),
                    (else_try),
                        # allow "next page" of heroes
                        (store_sub, reg2, reg10, num_loot_management_menu_heroes),
                        #  if already at last page
                        (ge, "$inventory_menu_offset", reg2),
                        # disable "next page" option
                        (disable_menu_option),
                    (try_end),
                ],
                "[Next page]",
                [
                    (val_add, "$inventory_menu_offset", num_loot_management_menu_heroes),
                    (jump_to_menu, "mnu_manage_loot_pool")
                ]
            ),
            ("leave",
                [],
                "{s20}",
                [
                    (call_script, "script_sod_recover_protected_items_from_loot_pool", "$pool_troop"),
                    (assign, "$g_camp_talk", 0),
                    (jump_to_menu, "$return_menu"),
                ]
            ),
        ]
    ),
]
