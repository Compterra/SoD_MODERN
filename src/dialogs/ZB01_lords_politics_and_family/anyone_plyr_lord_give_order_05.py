DIALOGS = [
[anyone|plyr, "lord_give_order",
   [
     (neg|troop_slot_eq, "$g_talk_troop", slot_troop_player_order_state, spai_undefined),
     ],
   "I won't need you for some time. You are free to do as you like.", "lord_give_order_stop",
   []],
]
