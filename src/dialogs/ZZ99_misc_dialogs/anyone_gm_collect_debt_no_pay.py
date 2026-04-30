DIALOGS = [
[anyone, "gm_collect_debt_no_pay", [], "Is this a joke?\
 I know full well that {s7} gave you the money, and I want every denar owed to me, {sir/madam}.\
 As far as I'm concerned, I hold you personally in my debt until I see that silver.", "close_window", [
     
	 (faction_get_slot, ":plyr_debt", "$g_talk_troop_faction", player_debt_to_faction),
	 (store_partner_quest, ":lords_quest"),
     (quest_get_slot, ":total_collected", ":lords_quest", slot_quest_target_amount),
     (val_mul, ":total_collected", 4),
     (val_div, ":total_collected", 5),
	 (val_add, ":plyr_debt", ":total_collected"),
	 (faction_set_slot, "$g_talk_troop_faction", player_debt_to_faction, ":plyr_debt"),
	 (store_partner_quest, ":lords_quest"),
     (call_script, "script_fail_quest", ":lords_quest"),
     (call_script, "script_end_quest", ":lords_quest"),
  (finish_mission),
     ]],
]
