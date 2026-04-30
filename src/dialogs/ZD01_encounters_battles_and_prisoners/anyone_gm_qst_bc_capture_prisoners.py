DIALOGS = [
[anyone, "gm_qst_bc_capture_prisoners", [],
   "Thank you, {playername}.", "gm_pretalk",
   [
	 (quest_get_slot, ":gold", "qst_bc_capture_prisoners", slot_quest_gold_reward),
	 (quest_get_slot, ":xp", "qst_bc_capture_prisoners", slot_quest_xp_reward),
     (add_xp_as_reward, ":xp"),
	 (call_script, "script_troop_add_gold", "trp_player", ":gold"),
	 (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 5),
	 (call_script, "script_succeed_quest", "$g_lords_quest"),
	 (call_script, "script_end_quest", "$g_lords_quest"),
    ]],
]
