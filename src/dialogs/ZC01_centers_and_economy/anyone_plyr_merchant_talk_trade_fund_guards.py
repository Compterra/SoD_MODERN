DIALOGS = [
[anyone|plyr, "merchant_trade_contract_options",
   [(eq, "$talk_context", tc_party_encounter),
    (neg|party_slot_ge, "$g_encountered_party", slot_party_sod_trade_contract, 1),
    (store_troop_gold, ":player_gold", "trp_player"),
    (ge, ":player_gold", 400)],
   "Take 400 denars and hire extra guards.", "merchant_trade_network_answer",
   [(call_script, "script_sod_player_charge_gold", 400),
    (call_script, "script_sod_trade_network_apply_player_contract", "$g_encountered_party", sod_trade_contract_guards, 400),
    (str_store_string, s20, "@The caravan master weighs the purse, then nods. Extra spears will ride close, and your name will be remembered if the road stays quiet.")]],
]
