MENUS = [
("quick_start", mnf_scale_picture|mnf_enable_hot_keys,
   "You are currently level {reg8}.  You have {reg5} renown, {reg3} honor, and {reg4} denars.^You have used {reg6} cheats in this game.^^{s1}",
   "none",
   [
    (set_background_mesh, "mesh_pic_payment"),

    (store_character_level, reg8, "trp_player"),
    # generate a list of your hero companions and their current levels.
    (party_get_num_companion_stacks, ":i", "p_main_party"),
    (assign, ":count", 0),
    (str_store_string, s2, "@Nobody"),
    (try_for_range, ":stack_no", 0, ":i"),
      (party_stack_get_troop_id, ":troop_id", "p_main_party", ":stack_no"),
      (is_between, ":troop_id", companions_begin, companions_end),
      # get the companion's name and level
      (call_script, "script_store_troop_name", s1, ":troop_id"),
      (store_character_level, reg1, ":troop_id"),
      (str_store_string, s1, "@{s1} (lvl {reg1})"),
      # build up the list from right to left
      (try_begin),
        (eq, ":count", 0),
        (str_store_string, s2, "@{s1}"),
      (else_try),
        (eq, ":count", 1),
        (str_store_string, s2, "@{s1} and {s2}"),
      (else_try),
        (str_store_string, s2, "@{s1}, {s2}"),
      (try_end),
      (val_add, ":count", 1),
    (try_end),
    (str_store_string, s1, "@You are travelling with: {s2}"),
    (troop_get_slot, reg5, "trp_player", slot_troop_renown),
    (assign, reg3, "$player_honor"),
    (store_troop_gold, reg4, "trp_player"),
	(assign, reg6, "$g_sod_cheat_mode_used"),
   ],
   [
    ("get_npcs", [], "Add companions to my party...", [(assign, "$inventory_menu_offset", 0), (jump_to_menu, "mnu_add_companions")]),
    ("give_xp", [(eq, "$g_sod_cheat_mode", 1), (store_character_level, reg1, "trp_player"), (val_mul, reg1, 500)], "Give me {reg1} XP.", [(add_xp_as_reward, reg1), (val_add,"$g_sod_cheat_mode_used", 1)]), #twan456
    ("give_denars", [(eq, "$g_sod_cheat_mode", 1)], "Give me 5000 denars.", [(call_script, "script_troop_add_gold", "trp_player", 5000), (val_add,"$g_sod_cheat_mode_used", 1)]),
    ("give_renown", [(eq, "$g_sod_cheat_mode", 1)], "Give me 50 renown.", [(call_script, "script_change_troop_renown", "trp_player", 50), (val_add,"$g_sod_cheat_mode_used", 1)]),
    ("give_honor", [(eq, "$g_sod_cheat_mode", 1)], "Give me 10 honor.", [(call_script, "script_change_player_honor", 10), (val_add,"$g_sod_cheat_mode_used", 1)]), #twan456
    ("take_honor", [], "Strip me of 10 honor.", [(call_script, "script_change_player_honor", -10)]),
    ("rechoose_banner", [], "Choose a different banner...", [(jump_to_menu, "mnu_banner_selection")]),
    ("quick_start_oracle", [(eq, "$g_sod_cheat_mode", 1)], "Consult oracle...", [(jump_to_menu, "mnu_quick_start_oracle"), (val_add, "$g_sod_cheat_mode_used", 1)]),
    ("done", [], "I think that ought to just about do it!", [(jump_to_menu, "mnu_camp")]),
   ]
  ),
]
