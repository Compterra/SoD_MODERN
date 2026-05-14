DIALOGS = [
[party_tpl|pt_jotnar_clan_warriors, "start", [],
   "Reinforcements! Finally! Quickly, the enemy is close.", "close_window", [
   (try_begin),
     (gt, "$g_encountered_party", 0),
     (neq, "$g_encountered_party", "p_main_party"),
     (party_is_active, "$g_encountered_party"),
     (party_get_template_id, ":encounter_template", "$g_encountered_party"),
     (eq, ":encounter_template", "pt_jotnar_clan_warriors"),
     (remove_party, "$g_encountered_party"),	
   (try_end),
   (jump_to_menu, "mnu_jotnar_clan_aid_warband"),
   (finish_mission),
   ]],
]
