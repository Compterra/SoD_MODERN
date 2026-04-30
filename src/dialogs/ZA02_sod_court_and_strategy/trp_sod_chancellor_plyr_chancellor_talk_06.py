DIALOGS = [
[trp_sod_chancellor|plyr, "chancellor_talk", [
	 (call_script, "script_get_number_of_factions_at_war_with_faction", "fac_player_supporters_faction"),
	 (gt, reg0, 0)], "I want to propose peace to one of the factions.", "chancellor_peace", []],
]
