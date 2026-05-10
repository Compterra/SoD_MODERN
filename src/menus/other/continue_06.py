MENUS = [
(
    "total_victory", 0,
    "You shouldn't be reading this... {s9}",
    "none",
    [
      #DEBUG - determine how this system works...
      #(assign, reg0, "$g_next_menu"),
      #(display_message, "@total_victory... $g_next_menu = {reg0}", debug_color),

      # We exploit the menu condition system below.
      # The conditions should make sure that always another screen or menu is called.
      (try_begin),
        (call_script, "script_total_victory_try_ally_thanks"),
        (eq, reg0, 1),
      (else_try),
        # Talk to enemy leaders
        (call_script, "script_total_victory_try_enemy_hero_resolution"),
        (eq, reg0, 1),
      (else_try),
        # Talk to freed heroes
        (call_script, "script_total_victory_try_freed_hero"),
        (eq, reg0, 1),
      (else_try),
        (eq, "$capture_screen_shown", 0),
        (assign, "$capture_screen_shown", 1),
        (call_script, "script_total_victory_prepare_capture_pool"),
        (party_get_num_companions, ":num_rescued_prisoners", "p_temp_party"),
        (party_get_num_prisoners, ":num_captured_enemies", "p_temp_party"),
        (store_add, ":total_capture_size", ":num_rescued_prisoners", ":num_captured_enemies"),
        (gt, ":total_capture_size", 0),
        (change_screen_exchange_with_party, "p_temp_party"),
      (else_try),
        (eq, "$loot_screen_shown", 0),
        (assign, "$loot_screen_shown", 1),
        (call_script, "script_sod_degrade_player_party_equipment_after_battle"),
        (call_script, "script_sod_companion_retinue_process_post_battle_hires"),
        (call_script, "script_total_victory_distribute_leftovers"),
        (troop_clear_inventory, "trp_temp_troop"),
        (call_script, "script_party_calculate_loot", "p_encountered_party_backup"),
        (gt, reg0, 0),
        (troop_sort_inventory, "trp_temp_troop"),
        # Autoloot: Instead of just displaying the loot screen, we display a loot management menu instead
        (try_begin),
          #MORDACHAI - only autoloot if you have companions to share the loot with!
          (call_script, "script_get_count_of_companions"),
          (gt, reg0, 0),
          (assign, "$return_menu", "mnu_total_victory"),
          (assign, "$inventory_menu_offset", 0), #MORDACHAI - bug fix (ensure we always start on page 1)
          (str_clear, s30),
          (jump_to_menu, "mnu_manage_loot_pool"),
        (else_try),
          (change_screen_loot, "trp_temp_troop"),
        (try_end),
        #end Autoloot
      (else_try),
        #finished all
        (call_script, "script_total_victory_finalize"),
        (try_begin),
          (eq, reg0, 1),
          (jump_to_menu, "$g_next_menu"),
        (try_end),
      (try_end),
	  (try_begin),
	  (eq, "$g_custom_banner", 1),
	  (troop_get_slot, ":flag_icon", "trp_player", slot_troop_custom_banner_map_flag_type),
          (try_begin),
            (ge, ":flag_icon", 0),
            (val_add, ":flag_icon", custom_banner_map_icons_begin),
            (party_set_banner_icon, "p_main_party", ":flag_icon"),
		  (else_try),
			(assign, ":flag_icon", 0),
			(val_add, ":flag_icon", custom_banner_map_icons_begin),
            (party_set_banner_icon, "p_main_party", ":flag_icon"),
          (try_end),
          (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
            (try_begin),
              (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
              (party_set_banner_icon, ":cur_center", ":flag_icon"),
            (try_end),
		  (try_end),
	(try_end),
    ],
    [
      ("continue", [], "Continue...", []),
    ]
  ),
]
