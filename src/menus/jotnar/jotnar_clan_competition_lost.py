MENUS = [
("jotnar_clan_competition_lost", 0,
  "Alas! You have lost the tournament.",
  "none",[],
  [
  ("continue",[],"Continue...",[
		(call_script, "script_end_quest", "qst_jotnar_clan_competition"),
		(jump_to_menu, "mnu_sod_merc_guild"),]),
	 ],),
]
