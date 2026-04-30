MISSION_TEMPLATES = [
(
    "jotnar_clan_arena", 0, -1,
    "You enter a melee fight in the arena.",
    [
      (11, mtef_visitor_source, af_override_all, aif_start_alarmed, 1, [
	  # itm_realbastarde, itm_nordic_helmet, itm_jotnar_clan_armor_1, itm_mail_boots, itm_mail_mittens
	  ]),
	  (12, mtef_visitor_source, af_override_all, 0, 1, [
	  # itm_dblhead_axe_2, itm_jotnar_clan_helm_2, itm_jotnar_clan_armor_3, itm_mail_boots, itm_mail_mittens
	  ]),
	  (13, mtef_visitor_source, af_override_all, 0, 1, [
	  # itm_sword_viking_2, itm_strong_bow, itm_barbed_arrows, itm_jotnar_clan_shield_3, itm_jotnar_clan_armor_5, itm_leather_boots, itm_leather_gloves, itm_jotnar_clan_horse_1
	  ]),
	  (14, mtef_visitor_source, af_override_all, 0, 1, [
	  # itm_dblhead_axe_1, itm_strong_bow, itm_bodkin_arrows, itm_jotnar_clan_shield_4, itm_jotnar_clan_armor_6, itm_villgloves1, itm_mail_boots, itm_jotnar_clan_horse_3
	  ]),
	  
      (21, mtef_visitor_source, af_override_all, 0, 1, [
	  # itm_realbastarde, itm_nordic_helmet, itm_jotnar_clan_armor_1, itm_mail_boots, itm_mail_mittens
	  ]),
	  (22, mtef_visitor_source, af_override_all, 0, 1, [
	  # itm_dblhead_axe_2, itm_jotnar_clan_helm_2, itm_jotnar_clan_armor_3, itm_mail_boots, itm_mail_mittens
	  ]),
	  (23, mtef_visitor_source, af_override_all, 0, 1, [
	  # itm_sword_viking_2, itm_strong_bow, itm_barbed_arrows, itm_jotnar_clan_shield_3, itm_jotnar_clan_armor_5, itm_leather_boots, itm_leather_gloves, itm_jotnar_clan_horse_1
	  ]),
	  (24, mtef_visitor_source, af_override_all, 0, 1, [
	  # itm_dblhead_axe_1, itm_strong_bow, itm_bodkin_arrows, itm_jotnar_clan_shield_4, itm_jotnar_clan_armor_6, itm_villgloves1, itm_mail_boots, itm_jotnar_clan_horse_3
	  ]),
	  
    ],
    [
      common_inventory_not_available,
	  # common_battle_horse_health,
      (ti_tab_pressed, 0, 0, [(display_message, "@Cannot leave now.", red)], []),
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_arena),
         ]),

      (1, 4, ti_once, [(this_or_next|main_hero_fallen), (num_active_teams_le, 1)],
       [
           (try_begin),
				(main_hero_fallen),
				(call_script, "script_change_troop_renown", "trp_player", -5),
				(quest_get_slot, reg1, "qst_jotnar_clan_competition", slot_quest_target_amount),
				(quest_get_slot, reg2, "qst_jotnar_clan_competition", slot_quest_gold_reward),
				(val_add, reg1, "$sod_jc_competition_lose_value"),
				(val_add, reg2, 1),
				(quest_set_slot, "qst_jotnar_clan_competition", slot_quest_target_amount, reg1),
				(quest_set_slot, "qst_jotnar_clan_competition", slot_quest_gold_reward, reg2),
           (else_try),
				(call_script, "script_change_troop_renown", "trp_player", 5),
				(quest_get_slot, reg1, "qst_jotnar_clan_competition", slot_quest_target_amount),
				(quest_get_slot, reg2, "qst_jotnar_clan_competition", slot_quest_gold_reward),
				(val_add, reg1, "$sod_jc_competition_win_value"),
				(val_add, reg2, 1),
				(quest_set_slot, "qst_jotnar_clan_competition", slot_quest_target_amount, reg1),
				(quest_set_slot, "qst_jotnar_clan_competition", slot_quest_gold_reward, reg2),
				(store_mul, ":gold_won", "$g_jotnar_clan_competition_bet", 2),
				(troop_add_gold, "trp_player", ":gold_won"),
           (try_end),
		   (finish_mission),
		   (jump_to_menu, "mnu_jotnar_clan_competition"),
           ]),
    ],
  ),
]
