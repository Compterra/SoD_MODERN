DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_party_encounter), (gt, "$g_encountered_party", 0), (party_is_active, "$g_encountered_party"), (eq, "$g_encountered_party_type", spt_kingdom_caravan), (ge, "$g_encountered_party_relation", 0)],
   "Hail, friend.", "merchant_talk", [(call_script, "script_sod_trade_network_initialize_caravan", "$g_encountered_party")]],
]
