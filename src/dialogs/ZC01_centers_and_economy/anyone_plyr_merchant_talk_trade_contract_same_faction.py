DIALOGS = [
[anyone|plyr, "merchant_talk",
   [(eq, "$talk_context", tc_party_encounter),
    (eq, "$g_encountered_party_faction", "$players_kingdom")],
   "Can my company take a share in this run?", "merchant_trade_contract_intro", []],
]
