DIALOGS = [
[anyone|plyr, "merchant_trade_contract_options",
   [(eq, "$talk_context", tc_party_encounter),
    (neg|party_slot_ge, "$g_encountered_party", slot_party_sod_trade_contract, 1),
    (store_troop_gold, ":player_gold", "trp_player"),
    (ge, ":player_gold", 600)],
   "Can I buy into this run? Here are 600 denars.", "merchant_trade_network_answer",
   [(call_script, "script_sod_player_charge_gold", 600),
    (call_script, "script_sod_trade_network_apply_player_contract", "$g_encountered_party", sod_trade_contract_cargo_space, 600),
    (str_store_string, s20, "@A little cargo space is yours now. If we reach the market whole, your share comes back fattened.")]],
]
