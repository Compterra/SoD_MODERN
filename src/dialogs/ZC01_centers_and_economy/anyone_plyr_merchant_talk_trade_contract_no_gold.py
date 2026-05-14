DIALOGS = [
[anyone|plyr, "merchant_trade_contract_options",
   [(eq, "$talk_context", tc_party_encounter),
    (neg|party_slot_ge, "$g_encountered_party", slot_party_sod_trade_contract, 1),
    (call_script, "script_sod_trade_network_get_contract_terms_to_regs", "$g_encountered_party", sod_trade_contract_insurance),
    (store_troop_gold, ":player_gold", "trp_player"),
    (lt, ":player_gold", reg0)],
   "I would back this run, but my purse is light.", "merchant_trade_network_answer",
   [(str_store_string, s20, "@Then keep your silver until it can do work. Even the smallest insurance mark on this road starts near {reg0} denars; guards, relief cargo, and profit stakes ask for more.")]],
]
