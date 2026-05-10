DIALOGS = [
[anyone|plyr, "town_merchant_talk", [(is_between, "$g_talk_troop", armor_merchants_begin, armor_merchants_end)],
   "I am looking for some equipment. Show me what you have.", "trade_requested_armor", []],
[anyone|plyr, "town_merchant_talk", [(is_between, "$g_talk_troop", armor_merchants_begin, armor_merchants_end)],
   "Can you repair damaged armor and shields carried by my company?", "town_merchant_talk", [
     (call_script, "script_sod_repair_player_party_equipment", sod_repair_service_armor),
   ]],
]
