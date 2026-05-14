DIALOGS = [
[anyone|plyr, "merchant_trade_contract_options",
   [(eq, "$talk_context", tc_party_encounter),
    (neg|party_slot_ge, "$g_encountered_party", slot_party_sod_trade_contract, 1),
    (call_script, "script_sod_trade_network_get_contract_terms_to_regs", "$g_encountered_party", sod_trade_contract_insurance),
    (store_troop_gold, ":player_gold", "trp_player"),
    (ge, ":player_gold", reg0)],
   "I will insure this run for {reg0} denars.", "merchant_trade_network_answer",
   [(call_script, "script_sod_trade_network_get_contract_terms_to_regs", "$g_encountered_party", sod_trade_contract_insurance),
    (call_script, "script_sod_player_charge_gold", reg0),
    (call_script, "script_sod_trade_network_apply_player_contract", "$g_encountered_party", sod_trade_contract_insurance, reg0),
    (str_store_string, s20, "@The caravan master smiles like a man who has seen too many wheels break. If the road turns cruel, at least the loss has a name.")]],
]
