DIALOGS = [
[anyone, "gm_hunt_down_fugitive_success", [],
   "And we'll all be a lot better off without him! Thank you, {playername},\
 for removing this long-festering thorn from my side. 'Tis good to know you can be trusted to handle things\
 with an appropriate level of tactfulness.", "gm_pretalk",
   [
     (add_xp_as_reward, 600),
	 (call_script, "script_troop_add_gold", "trp_player", 300),
	 (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 3),
	 (call_script, "script_succeed_quest", "$g_lords_quest"),
	 (call_script, "script_end_quest", "$g_lords_quest"),
    ]],
]
