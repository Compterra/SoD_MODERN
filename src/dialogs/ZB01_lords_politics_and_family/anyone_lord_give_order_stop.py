DIALOGS = [
[anyone, "lord_give_order_stop",
   [],
   "All right. I will do that.", "lord_pretalk",
   [
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_state, spai_undefined),
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_object, -1),
     (troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
     (try_begin),
       (gt, ":party_no", 0),
       (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
       (party_set_slot, ":party_no", slot_party_commander_party, -1),
     (try_end),
     ]],
]
