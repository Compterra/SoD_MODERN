DIALOGS = [
[anyone|plyr, "merchant_trade_contract_options",
   [(eq, "$talk_context", tc_party_encounter),
    (neg|party_slot_ge, "$g_encountered_party", slot_party_sod_trade_contract, 1),
    (store_troop_gold, ":player_gold", "trp_player"),
    (ge, ":player_gold", 250)],
   "I will insure this run for 250 denars.", "merchant_trade_network_answer",
   [(call_script, "script_sod_player_charge_gold", 250),
    (call_script, "script_sod_trade_network_apply_player_contract", "$g_encountered_party", sod_trade_contract_insurance, 250),
    (str_store_string, s20, "@The caravan master smiles like a man who has seen too many wheels break. If the road turns cruel, at least the loss has a name.")]],
]
