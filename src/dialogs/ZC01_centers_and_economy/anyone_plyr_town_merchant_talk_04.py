DIALOGS = [
[anyone|plyr, "town_merchant_talk", [],
   "Sell low-value spare gear carried by my companions.", "town_merchant_talk", [
     (call_script, "script_sod_auto_sell_companion_inventory_to_merchant", "$g_talk_troop", 300),
   ]],
[anyone|plyr, "town_merchant_talk", [],
   "Sell ordinary spare gear carried by my companions.", "town_merchant_talk", [
     (call_script, "script_sod_auto_sell_companion_inventory_to_merchant", "$g_talk_troop", 600),
   ]],
[anyone|plyr, "town_merchant_talk", [], "Tell me. What are people talking about these days?", "merchant_gossip", []],
]
