DIALOGS = [
[anyone|plyr, "goods_merchant_talk", [],
   "Buy up to four food types my party is missing.", "goods_merchant_talk", [
     (call_script, "script_sod_auto_buy_food_from_merchant", "$g_talk_troop"),
   ]],
[anyone|plyr, "goods_merchant_talk", [], "What goods should I buy here to trade with other towns?", "trade_info_request", []],
]
