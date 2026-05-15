DIALOGS = [
[anyone, "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_seneschal),
                    (eq, "$talk_context", tc_siege_won_seneschal),
                    (str_store_party_name, s68, "$g_encountered_party"),
                    ],
   "I must congratulate you on your victory, my {lord/lady}. Welcome to {s68}.\
 We, the housekeepers of this castle, are at your service.", "siege_won_seneschal_1", []],
]
