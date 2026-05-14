DIALOGS = [
[anyone, "lord_give_order_answer",
   [
     (assign, ":continue", 0),
     (try_begin),
       (troop_slot_ge, "$g_talk_troop", slot_troop_readiness_to_follow_orders, 60),
       (assign, ":continue", 1),
     (else_try),
       (troop_slot_ge, "$g_talk_troop", slot_troop_readiness_to_follow_orders, 10),
       (neg|troop_slot_eq, "$g_talk_troop", slot_troop_player_order_state, spai_undefined),
       (assign, ":continue", 1),
     (try_end),
     (troop_get_slot, ":party_no", "$g_talk_troop", slot_troop_leaded_party),
     (this_or_next|le, ":party_no", 0),
     (eq, ":continue", 0),
     #Meaning that hero does not want to follow player orders for a while.
     ],
   "Not now. My own business has teeth in it, and I cannot pull away.", "lord_pretalk",
   [
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_state, spai_undefined),
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_object, -1),
     ]],
]
