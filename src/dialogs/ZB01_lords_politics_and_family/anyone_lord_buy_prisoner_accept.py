DIALOGS = [
[anyone, "lord_buy_prisoner_accept", [],
   "Excellent! Here's your {reg6} denars.\
 I'll send some men to take him to our prison with due haste.", "lord_pretalk", [
     (call_script, "script_remove_troop_from_prison", "$prisoner_lord_to_buy"),
     (call_script, "script_troop_add_gold", "trp_player", "$temp"),
     (try_begin),
       (gt, "$g_encountered_party", 0),
       (party_is_active, "$g_encountered_party"),
       (party_add_prisoners, "$g_encountered_party", "$prisoner_lord_to_buy", 1),
       (troop_set_slot, "$prisoner_lord_to_buy", slot_troop_prisoner_of_party, "$g_encountered_party"),
       (call_script, "script_sod_runtime_trace_event", 7, "$g_encountered_party", "$prisoner_lord_to_buy"),
     (try_end),
     ]],
]
