DIALOGS = [
[anyone|plyr, "merchant_trade_contract_options",
   [(eq, "$talk_context", tc_party_encounter),
    (party_slot_ge, "$g_encountered_party", slot_party_sod_trade_contract, 1)],
   "Can I make another arrangement for this run?", "merchant_trade_network_answer",
   [(str_store_string, s20, "@We already have your mark on this run. Let the first bargain reach market before loading another promise on the same wagons.")]],
]
