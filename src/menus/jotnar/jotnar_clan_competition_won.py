MENUS = [
("jotnar_clan_competition_won", 0,
  "Congratulations! You have won the tournament.",
  "none",[],
  [
  ("continue",[],"Continue...",[
		(call_script, "script_end_quest", "qst_jotnar_clan_competition"),
		(add_xp_as_reward, 1000),
		(call_script, "script_change_troop_renown", "trp_player", 15),
		(call_script, "script_change_player_relation_with_troop", jotnar_clan_guild_master, 5),
	  (jump_to_menu, "mnu_sod_merc_guild"),]),
	 ],),
]
