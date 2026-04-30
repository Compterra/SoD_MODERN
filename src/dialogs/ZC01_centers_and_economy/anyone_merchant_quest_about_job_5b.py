DIALOGS = [
[anyone, "merchant_quest_about_job_5b", [],
   "Do you expect me to believe that? You are going to pay that ransom fee back! Go and bring the money now!",
   "close_window", [(quest_get_slot, ":quest_target_amount", "qst_serpent_host_free_spy", slot_quest_target_amount),
                   (faction_get_slot, ":cur_debt", "$g_talk_troop_faction", player_debt_to_faction),
				   (val_add, ":cur_debt", ":quest_target_amount"),
				   (faction_set_slot, "$g_talk_troop_faction", player_debt_to_faction, ":cur_debt"),
                  
  (finish_mission), ]],
]
