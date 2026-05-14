DIALOGS = [
[anyone,"gm_hire8", [				
		(call_script, "script_merc_calculate_hire_quote", "$g_talk_troop_faction", "$temp1", "$temp_proportion", "$temp2", "$temp3"),
		(assign, "$merc_cost", reg0),
		(assign, reg19, reg0),
		(assign, "$g_sod_merc_player_hire_market_limit", reg2),
		(call_script, "script_merc_describe_guild_offer", "$g_talk_troop_faction"),
                        ],"Very well. The retainer for such a party is {reg19} denars.^^You are paying for {s50} and {s51}. Our base terms are {s52}, and your standing adds {s53}.^^{s54}^{s55}^{s56}^{s57}^{s58}","gm_hire9", []],
]
