DIALOGS = [
[anyone, "lost_sh_spy_debt", [(gt, "$g_sod_lost_rescue_repayment_amount", 0)],
   "Then the debt stands with my faction. Bring the money when you have it.",
   "close_window", [(faction_get_slot, ":cur_debt", "$g_talk_troop_faction", player_debt_to_faction),
				   (val_add, ":cur_debt", "$g_sod_lost_rescue_repayment_amount"),
				   (faction_set_slot, "$g_talk_troop_faction", player_debt_to_faction, ":cur_debt"),
                   (assign, "$g_sod_lost_rescue_repayment_amount", 0),
                  
  (finish_mission), ]],
]
