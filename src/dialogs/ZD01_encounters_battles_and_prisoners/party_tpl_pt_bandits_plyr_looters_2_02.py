DIALOGS = [
[party_tpl|pt_bandits|plyr, "looters_2", [[store_character_level, reg(1), "trp_player"], [ge, reg(1), 4]], "You picked the wrong purse and the wrong road. Take your lesson in steel.", "close_window",
   [
     (assign, "$g_enemy_party", "$g_encountered_party"),
     (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
     (encounter_attack),
   ]],
]
