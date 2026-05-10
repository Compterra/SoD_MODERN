DIALOGS = [
[anyone|plyr, "sod_slaver_buy_slaves_offer",
   [
     (call_script, "script_sod_slavers_store_slave_purchase_quote"),
     (gt, reg2, 0),
     (store_troop_gold, ":player_gold", "trp_player"),
     (lt, ":player_gold", reg3),
   ],
   "I cannot afford that.", "close_window", []],
]
