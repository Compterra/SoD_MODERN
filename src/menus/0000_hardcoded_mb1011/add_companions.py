MENUS = [
("add_companions", mnf_scale_picture|mnf_enable_hot_keys,
   "{s98}.^^Who would you like to add?",
   "none",
    [
      (set_background_mesh, "mesh_pic_payment"),
      # generate a list of your hero companions and their current levels.
      (party_get_num_companion_stacks, ":i", "p_main_party"),
      (assign, ":count", 0),
      (str_store_string, s69, "@Nobody"),
      (try_for_range, ":stack_no", 0, ":i"),
        (party_stack_get_troop_id, ":troop_id", "p_main_party", ":stack_no"),
        (is_between, ":troop_id", companions_begin, companions_end),
        # get the companion's name and level
        (call_script, "script_store_troop_name", s68, ":troop_id"),
        (store_character_level, reg1, ":troop_id"),
        (str_store_string, s70, "@{s68} (lvl {reg1})"),
        # build up the list from right to left
        (try_begin),
          (eq, ":count", 0),
          (str_store_string_reg, s69, s70),
        (else_try),
          (str_store_string, s97, "@{s70}^{s69}"),
          (str_store_string_reg, s69, s97),
        (try_end),
        (val_add, ":count", 1),
      (try_end),
      (str_store_string, s98, "@You are travelling with:^{s69}"),

      # generate the list of heros that aren't currently in your party, and let the player select them
      # concept & basic code ripped from - Fisheye's Autoloot -
      (assign, reg11, 0),
      (assign, reg12, 0),
      (assign, reg13, 0),
      (assign, reg14, 0),
      (assign, reg15, 0),
      (assign, reg16, 0),

      # count the number of available companions
      (assign, reg10, 0),
      (try_for_range, ":companion", companions_begin, companions_end),
        (troop_slot_eq, ":companion", slot_troop_occupation, 0),
        (val_add, reg10, 1),
      (try_end),

      # fall back a page if the current page no longer exists
      (try_begin),
        (eq, "$inventory_menu_offset", reg10),
        (val_sub, "$inventory_menu_offset", 6),
        (val_max, "$inventory_menu_offset", 0),
      (try_end),

      (assign, reg10, 0),
      (try_for_range, ":companion", companions_begin, companions_end),
        # only include heros that aren't currently a part of our party
        (troop_slot_eq, ":companion", slot_troop_occupation, 0),
        # count the number of such heros, and keep track of our current index into them
        (val_add, reg10, 1),
        (try_begin),
          (store_add, ":menu_index", "$inventory_menu_offset", 1),
          (eq, reg10, ":menu_index"),
          (assign, reg11, ":companion"),
          (call_script, "script_store_troop_name", 11, ":companion"),
        (else_try),
          (store_add, ":menu_index", "$inventory_menu_offset", 2),
          (eq, reg10, ":menu_index"),
          (assign, reg12, ":companion"),
          (call_script, "script_store_troop_name", 12, ":companion"),
        (else_try),
          (store_add, ":menu_index", "$inventory_menu_offset", 3),
          (eq, reg10, ":menu_index"),
          (assign, reg13, ":companion"),
          (call_script, "script_store_troop_name", 13, ":companion"),
        (else_try),
          (store_add, ":menu_index", "$inventory_menu_offset", 4),
          (eq, reg10, ":menu_index"),
          (assign, reg14, ":companion"),
          (call_script, "script_store_troop_name", 14, ":companion"),
        (else_try),
          (store_add, ":menu_index", "$inventory_menu_offset", 5),
          (eq, reg10, ":menu_index"),
          (assign, reg15, ":companion"),
          (call_script, "script_store_troop_name", 15, ":companion"),
        (else_try),
          (store_add, ":menu_index", "$inventory_menu_offset", 6),
          (eq, reg10, ":menu_index"),
          (assign, reg16, ":companion"),
          (call_script, "script_store_troop_name", 16, ":companion"),
        (try_end),
      (try_end),
      # reg10 now contains total num of heroes available to interact with (not yet in party)

      (try_begin),
        (gt, reg10, 0),
        (store_add, reg1, "$inventory_menu_offset", 1),
        (store_add, reg2, "$inventory_menu_offset", 6),
        (val_min, reg2, reg10),
        (str_store_string_reg, s97, s98),
        (str_store_string, s98, "@{s97}^^(showing {reg1} through {reg2} of {reg10})"),
      (else_try),
        (str_store_string_reg, s97, s98),
        (str_store_string, s98, "@{s97}^^No unjoined companions are currently available."),
      (try_end),
    ],
    [
      ("npc_1", [(gt, reg11, 0)], "{s11}", [(call_script, "script_setup_troop_meeting", reg11, 0)]),
      ("npc_2", [(gt, reg12, 0)], "{s12}", [(call_script, "script_setup_troop_meeting", reg12, 0)]),
      ("npc_3", [(gt, reg13, 0)], "{s13}", [(call_script, "script_setup_troop_meeting", reg13, 0)]),
      ("npc_4", [(gt, reg14, 0)], "{s14}", [(call_script, "script_setup_troop_meeting", reg14, 0)]),
      ("npc_5", [(gt, reg15, 0)], "{s15}", [(call_script, "script_setup_troop_meeting", reg15, 0)]),
      ("npc_6", [(gt, reg16, 0)], "{s16}", [(call_script, "script_setup_troop_meeting", reg16, 0)]),
      ("npc_next",
        [
          #base for next page
          (store_add, ":next_page", "$inventory_menu_offset", 6),
          (try_begin),
            # don't give this option if we're on the last page
            (ge, ":next_page", reg10),
            (disable_menu_option),
          (try_end),
        ],
        "[Next page]",
        [
          (val_add, "$inventory_menu_offset", 6),
          (jump_to_menu, "mnu_add_companions"),
        ]
      ),
      ("npc_previous",
        [
          (try_begin),
            # don't give this option if we're on the first page
            (eq, "$inventory_menu_offset", 0),
            (disable_menu_option),
          (try_end),
        ],
        "[Previous page]",
        [
          (val_sub, "$inventory_menu_offset", 6),
          (jump_to_menu, "mnu_add_companions"),
        ]
      ),
      ("npc_nvm", [], "That's enough companions, thanks.", [(jump_to_menu, "mnu_quick_start")]),
    ]
  ),
]
