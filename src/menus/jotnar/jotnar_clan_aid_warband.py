MENUS = [
("jotnar_clan_aid_warband", 0,
  "The enemy charges from the village.",
  "none",[],
  [
  ("continue",[],"Continue...",[
		(quest_get_slot, ":cur_village", "qst_jotnar_clan_aid_warband", slot_quest_target_center),
		(quest_get_slot, ":cur_troop", "qst_jotnar_clan_aid_warband", slot_quest_target_troop),
        (party_get_slot, ":scene_to_use", ":cur_village", slot_castle_exterior),
		(assign, "$g_encountered_party", ":cur_village"),
        (modify_visitors_at_site, ":scene_to_use"),
		(try_begin),
		   (le, ":cur_troop", 0),                    #twan456
		   (assign, ":cur_troop", "trp_bandit"),
		(try_end),   
        (reset_visitors),
        (set_visitors, 0, ":cur_troop", 40),
		(set_visitors, 2, "trp_jotnar_clan_armsman", 15),
		(set_party_battle_mode),
        (set_battle_advantage, 0),
        (assign, "$g_battle_result", 0),
        (set_jump_mission, "mt_village_attack_bandits"),
        (jump_to_scene, ":scene_to_use"),
        (assign, "$g_next_menu", "mnu_village_jotnar_clan_result"),
		(jump_to_menu, "mnu_battle_debrief"),
        (assign, "$g_mt_mode", vba_normal),
        (change_screen_mission),]),
	 ],),
]
