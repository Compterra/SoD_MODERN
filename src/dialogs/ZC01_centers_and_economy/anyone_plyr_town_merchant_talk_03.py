DIALOGS = [
[anyone|plyr, "town_merchant_talk", [(is_between, "$g_talk_troop", horse_merchants_begin, horse_merchants_end)],
   "I am thinking of buying a horse.", "trade_requested_horse", []],
[anyone|plyr, "town_merchant_talk", [(is_between, "$g_talk_troop", horse_merchants_begin, horse_merchants_end)],
   "Can you tend to injured mounts in my company?", "town_merchant_talk", [
     (call_script, "script_sod_repair_player_party_equipment", sod_repair_service_horses),
   ]],
]
