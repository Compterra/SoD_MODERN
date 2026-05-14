DIALOGS = [
[anyone|plyr, "town_merchant_talk", [(is_between, "$g_talk_troop", armor_merchants_begin, armor_merchants_end)],
   "Show me armor worth trusting when the first arrow lands.", "trade_requested_armor", []],
[anyone|plyr, "town_merchant_talk", [(is_between, "$g_talk_troop", armor_merchants_begin, armor_merchants_end),
                                      (party_slot_ge, "$current_town", slot_center_has_blacksmith, 1)],
   "My company's armor has taken honest blows. Make it fit for another fight.", "town_merchant_talk", [
     (call_script, "script_sod_repair_player_party_equipment", sod_repair_service_armor),
   ]],
]
