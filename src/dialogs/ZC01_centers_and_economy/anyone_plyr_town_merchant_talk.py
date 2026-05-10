DIALOGS = [
[anyone|plyr, "town_merchant_talk", [(is_between, "$g_talk_troop", weapon_merchants_begin, weapon_merchants_end)],
   "I want to buy a new weapon. Show me your wares.", "trade_requested_weapons", []],
[anyone|plyr, "town_merchant_talk", [(is_between, "$g_talk_troop", weapon_merchants_begin, weapon_merchants_end)],
   "Can you repair damaged weapons carried by my company?", "town_merchant_talk", [
     (call_script, "script_sod_repair_player_party_equipment", sod_repair_service_weapons),
   ]],
]
