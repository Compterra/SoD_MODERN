DIALOGS = [
[anyone, "lord_start", [(neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                         (troop_get_slot, ":cur_debt", "$g_talk_troop", slot_troop_player_debt),
                         (gt, ":cur_debt", 0),
                         (assign, reg1, ":cur_debt")],
   "I think you owe me {reg1} denars, {playername}. Do you intend to pay your debt anytime soon?", "lord_pay_debt_2", []],
]
