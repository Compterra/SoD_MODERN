DIALOGS = [
[trp_sod_marshal, "marshal_campaign2", [], "All right then. I will send messengers and tell everyone to come here.", "marshal_talk",
    [(faction_set_slot, "$players_kingdom", slot_faction_ai_state, sfai_gathering_army),
     (assign, "$g_recalculate_ais", 1), ]],
]
