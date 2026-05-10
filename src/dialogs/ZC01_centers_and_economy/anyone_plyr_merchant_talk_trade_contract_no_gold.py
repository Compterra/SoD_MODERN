DIALOGS = [
[anyone|plyr, "merchant_trade_contract_options",
   [(eq, "$talk_context", tc_party_encounter),
    (neg|party_slot_ge, "$g_encountered_party", slot_party_sod_trade_contract, 1),
    (store_troop_gold, ":player_gold", "trp_player"),
    (lt, ":player_gold", 250)],
   "I would back this run, but my purse is light.", "merchant_trade_network_answer",
   [(str_store_string, s20, "@Then keep your silver until it can do work. Insurance starts at 250 denars; guards, relief cargo, and profit stakes ask for more.")]],
]
