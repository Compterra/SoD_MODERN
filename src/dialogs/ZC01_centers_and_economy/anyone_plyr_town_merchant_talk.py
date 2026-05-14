DIALOGS = [
[anyone|plyr, "town_merchant_talk", [(is_between, "$g_talk_troop", weapon_merchants_begin, weapon_merchants_end)],
   "Show me steel that has not yet disappointed its owner.", "trade_requested_weapons", []],
[anyone|plyr, "town_merchant_talk", [(is_between, "$g_talk_troop", weapon_merchants_begin, weapon_merchants_end),
                                      (party_slot_ge, "$current_town", slot_center_has_blacksmith, 1)],
   "My company's weapons have earned scars. Put an edge back on them.", "town_merchant_talk", [
     (call_script, "script_sod_repair_player_party_equipment", sod_repair_service_weapons),
   ]],
]
