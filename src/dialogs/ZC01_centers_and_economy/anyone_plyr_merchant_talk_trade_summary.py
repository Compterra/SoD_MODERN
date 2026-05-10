DIALOGS = [
[anyone|plyr, "merchant_talk", [(eq, "$talk_context", tc_party_encounter)],
   "What news travels with these wagons?", "merchant_trade_network_answer",
   [(call_script, "script_sod_trade_network_describe_caravan_to_s20", "$g_encountered_party", 0)]],
]
