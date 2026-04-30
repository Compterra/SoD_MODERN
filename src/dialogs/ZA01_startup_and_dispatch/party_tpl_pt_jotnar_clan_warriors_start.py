DIALOGS = [
[party_tpl|pt_jotnar_clan_warriors, "start", [],
   "Reinforcements! Finally! Quickly, the enemy is close.", "close_window", [
   (remove_party, "$g_encountered_party"),	
   (jump_to_menu, "mnu_jotnar_clan_aid_warband"),
   ]],
]
