DIALOGS = [
[anyone|auto_proceed, "lord_give_order_answer",
   [],
   ".", "lord_give_order_answer_2",
   [
     (troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
     (call_script, "script_party_set_ai_state", ":party_no", "$temp", "$temp_2"),
     (try_begin),
       (eq, "$temp", spai_accompanying_army),
       (party_set_slot, ":party_no", slot_party_commander_party, "$temp_2"),
     (else_try),
       (party_set_slot, ":party_no", slot_party_commander_party, -1),
     (try_end),
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_state, "$temp"),
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_object, "$temp_2"),
     #Checking if the order is accepted by the ai
     (call_script, "script_recalculate_ai_for_troop", "$g_talk_troop"),
     ]],
]
