DIALOGS = [
[anyone|plyr, "merchant_trade_contract_options",
   [(eq, "$talk_context", tc_party_encounter),
    (neg|party_slot_ge, "$g_encountered_party", slot_party_sod_trade_contract, 1),
    (store_troop_gold, ":player_gold", "trp_player"),
    (ge, ":player_gold", 500)],
   "Carry 500 denars of relief cargo where it is needed.", "merchant_trade_network_answer",
   [(call_script, "script_sod_player_charge_gold", 500),
    (call_script, "script_sod_trade_network_apply_player_contract", "$g_encountered_party", sod_trade_contract_relief, 500),
    (str_store_string, s20, "@Relief cargo rides under your mark. It may not sing like profit, but hungry markets remember bread.")]],
]
