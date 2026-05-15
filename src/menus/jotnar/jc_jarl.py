MENUS = [
(
    "jc_choose_opponent", 0,
    "Choose your next opponent. The challenged fighter chooses the weapons, armor, and horses.^^The values in brackets show standing gained or lost after the duel.",
    "none",
    [],
    [
      ("jc_jarl", [], "Jarl (Win +1, Lose -2)",
       [
	   (quest_set_slot, "qst_jotnar_clan_competition", slot_quest_target_troop, "trp_jotnar_clan_jarl"),
	   (assign, "$sod_jc_competition_win_value", 1),
	   (assign, "$sod_jc_competition_lose_value", -2),
	   (jump_to_menu, "mnu_jc_choose_bet"),
        ]),
		("jc_einherjar", [], "Einherjar (Win +2, Lose -1)",
       [
	   (quest_set_slot, "qst_jotnar_clan_competition", slot_quest_target_troop, "trp_jotnar_clan_einherjar"),
	   (assign, "$sod_jc_competition_win_value", 2),
	   (assign, "$sod_jc_competition_lose_value", -1),
	   (jump_to_menu, "mnu_jc_choose_bet"),
        ]),
		("jc_valkyrie", [], "Valkyrie (Win +1, Lose -2)",
       [
	   (quest_set_slot, "qst_jotnar_clan_competition", slot_quest_target_troop, "trp_jotnar_clan_valkyrie"),
	   (assign, "$sod_jc_competition_win_value", 1),
	   (assign, "$sod_jc_competition_lose_value", -2),
	   (jump_to_menu, "mnu_jc_choose_bet"),
        ]),
		("jc_disir", [], "Disir (Win +2, Lose -2)",
       [
	   (quest_set_slot, "qst_jotnar_clan_competition", slot_quest_target_troop, "trp_jotnar_clan_disir"),
	   (assign, "$sod_jc_competition_win_value", 2),
	   (assign, "$sod_jc_competition_lose_value", -2),
	   (jump_to_menu, "mnu_jc_choose_bet"),
        ]),
	  ("back", [], "Back.",
       [(jump_to_menu, "mnu_jotnar_clan_competition"),
        ]),
     ]
  ),
]
