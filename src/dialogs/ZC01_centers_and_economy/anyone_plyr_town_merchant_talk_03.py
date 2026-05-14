DIALOGS = [
[anyone|plyr, "town_merchant_talk", [(is_between, "$g_talk_troop", horse_merchants_begin, horse_merchants_end)],
   "Show me horses with road left in them.", "trade_requested_horse", []],
[anyone|plyr, "town_merchant_talk", [(is_between, "$g_talk_troop", horse_merchants_begin, horse_merchants_end),
                                      (party_slot_ge, "$current_town", slot_center_has_stables, 1)],
   "My mounts are carrying old pain. See what can be mended.", "town_merchant_talk", [
     (call_script, "script_sod_repair_player_party_equipment", sod_repair_service_horses),
   ]],
]
