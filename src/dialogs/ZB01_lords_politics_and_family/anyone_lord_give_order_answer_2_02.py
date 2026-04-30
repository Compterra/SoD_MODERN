DIALOGS = [
[anyone, "lord_give_order_answer_2",
   [
     #Meaning that the AI decision function did not follow the order.
     ],
   "I am sorry, it is not possible for me to do that.", "lord_pretalk",
   [
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_state, spai_undefined),
     (troop_set_slot, "$g_talk_troop", slot_troop_player_order_object, -1),

     ]],
]
