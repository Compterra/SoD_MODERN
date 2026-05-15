MENUS = [
(
    "jc_get_choosen", 0,
    "{s2} challenges you to a duel. As the challenged fighter, you choose the equipment.",
    "none",
    [
	(assign, reg0, "trp_jotnar_clan_jarl"),
	(assign, reg1, "trp_jotnar_clan_einherjar"),
	(assign, reg2, "trp_jotnar_clan_valkyrie"),
	(assign, reg3, "trp_jotnar_clan_disir"),
	(shuffle_range, 0, 4),
	(try_begin),
		(eq, reg1, "trp_jotnar_clan_jarl"),
	   (assign, "$sod_jc_competition_win_value", 1),
	   (assign, "$sod_jc_competition_lose_value", -2),
	(else_try),
		(eq, reg1, "trp_jotnar_clan_einherjar"),
	   (assign, "$sod_jc_competition_win_value", 2),
	   (assign, "$sod_jc_competition_lose_value", -1),
	(else_try),
		(eq, reg1, "trp_jotnar_clan_valkyrie"),
	   (assign, "$sod_jc_competition_win_value", 1),
	   (assign, "$sod_jc_competition_lose_value", -2),
	(else_try),
	   (assign, "$sod_jc_competition_win_value", 2),
	   (assign, "$sod_jc_competition_lose_value", -2),
	(try_end),
	(quest_set_slot, "qst_jotnar_clan_competition", slot_quest_target_troop, reg1),
	(str_store_troop_name, s2, reg1),
	],
    [
  ("wep_set_1", [], "Medium Armor, Two Handed Sword", [
	(assign, "$jc_wep_set", 1),
	(jump_to_menu, "mnu_player_choosen_select_bet"),]),
  ("wep_set_2", [], "Medium Armor, Two Handed Axe", [
	(assign, "$jc_wep_set", 2),
	(jump_to_menu, "mnu_player_choosen_select_bet"),]),
  ("wep_set_3", [], "Light Armor, One Handed Sword, Shield, Bow and Arrows, Horse", [
	(assign, "$jc_wep_set", 3),
	(jump_to_menu, "mnu_player_choosen_select_bet"),]),
  ("wep_set_4", [], "Medium Armor, One Handed Axe, Shield, Bow and Arrows, Horse", [
	(assign, "$jc_wep_set", 4),
	(jump_to_menu, "mnu_player_choosen_select_bet"),]),
	
	  ("back", [], "Reject the challenge.",
       [(jump_to_menu, "mnu_jotnar_clan_competition"),
        (call_script, "script_change_troop_renown", "trp_player", -3),
		]),
     ]
  ),
]
