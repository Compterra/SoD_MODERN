DIALOGS = [
[anyone, "lord_give_order_disband_army",
   [],
   "All right. I will let everyone know that they are released from duty.", "lord_pretalk",
   [
     (faction_set_slot, "$players_kingdom", slot_faction_ai_state, sfai_default),
     (try_for_range, ":cur_troop", kingdom_heroes_begin, kingdom_heroes_end),
       (troop_get_slot, ":party_no", ":cur_troop", slot_troop_leaded_party),
       (gt, ":party_no", 0),
       (party_slot_eq, ":party_no", slot_party_commander_party, "p_main_party"),
       (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
       (party_set_slot, ":party_no", slot_party_commander_party, -1),
     (try_end),
     (assign, "$g_recalculate_ais", 1),
     ]],
]
