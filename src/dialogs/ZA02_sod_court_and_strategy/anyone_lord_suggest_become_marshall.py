DIALOGS = [
[anyone, "lord_suggest_become_marshall", [],
   "Alright then.", "lord_pretalk",
   [
     (faction_set_slot, "$g_talk_troop_faction", slot_faction_marshall, "trp_player"),
     (faction_set_slot, "$g_talk_troop_faction", slot_faction_ai_state, sfai_default),
     (assign, "$g_recalculate_ais", 1),
     ]],
]
