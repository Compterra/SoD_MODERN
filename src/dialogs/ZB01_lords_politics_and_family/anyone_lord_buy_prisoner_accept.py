DIALOGS = [
[anyone, "lord_buy_prisoner_accept", [],
   "Excellent! Here's your {reg6} denars.\
 I'll send some men to take him to our prison with due haste.", "lord_pretalk", [
     (remove_troops_from_prisoners,  "$prisoner_lord_to_buy", 1),
     (call_script, "script_troop_add_gold", "trp_player", "$temp"),
     (party_add_prisoners, "$g_encountered_party", "$prisoner_lord_to_buy", 1),
     (troop_set_slot, "$prisoner_lord_to_buy", slot_troop_prisoner_of_party, "$g_encountered_party"),
     ]],
]
