DIALOGS = [
[anyone, "lord_give_order_call_to_arms",
   [],
   "All right then. I will send messengers and tell everyone to come here.", "lord_pretalk",
   [
     (faction_set_slot, "$players_kingdom", slot_faction_ai_state, sfai_gathering_army),
     (assign, "$g_recalculate_ais", 1),
     ]],
]
