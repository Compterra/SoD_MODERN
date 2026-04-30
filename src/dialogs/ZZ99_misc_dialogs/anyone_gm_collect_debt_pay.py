DIALOGS = [
[anyone, "gm_collect_debt_pay", [],
   "I must admit I'm impressed, {playername}. I had lost hope of ever getting this money back. Please accept my sincere thanks.", "gm_pretalk", [
	 (store_partner_quest, ":lords_quest"),
     (quest_get_slot, ":total_collected", ":lords_quest", slot_quest_target_amount),
     (val_mul, ":total_collected", 4),
     (val_div, ":total_collected", 5),
	 (troop_remove_gold, "trp_player", ":total_collected"),
     (play_sound, "snd_money_paid"),
     (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 3),
     (add_xp_as_reward, 300),
     (call_script, "script_succeed_quest", ":lords_quest"),
     (call_script, "script_end_quest", ":lords_quest")
     ]],
]
