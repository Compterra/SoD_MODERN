DIALOGS = [
[anyone|plyr, "merchant_talk",
   [(eq, "$talk_context", tc_party_encounter),
    (neg|eq, "$g_encountered_party_faction", "$players_kingdom")],
   "Could my company take a share in this run?", "merchant_trade_contract_refused", []],
]
