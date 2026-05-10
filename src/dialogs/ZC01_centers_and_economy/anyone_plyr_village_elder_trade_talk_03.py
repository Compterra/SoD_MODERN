DIALOGS = [
[anyone|plyr, "village_elder_trade_talk", [],
   "Buy the food types my party is missing.", "village_elder_trade_talk", [
     (call_script, "script_sod_auto_buy_food_from_merchant", "$g_talk_troop"),
   ]],
[anyone|plyr, "village_elder_trade_talk", [], "Keep the storehouse sealed. I do not need supplies today.", "village_elder_pretalk", []],
]
