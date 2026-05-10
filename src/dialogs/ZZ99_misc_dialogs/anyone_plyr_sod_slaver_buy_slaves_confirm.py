DIALOGS = [
[anyone|plyr, "sod_slaver_buy_slaves_offer",
   [
     (call_script, "script_sod_slavers_store_slave_purchase_quote"),
     (gt, reg2, 0),
     (store_troop_gold, ":player_gold", "trp_player"),
     (ge, ":player_gold", reg3),
   ],
   "Buy them.", "sod_slaver_buy_slaves_done",
   [
     (call_script, "script_sod_slavers_store_slave_purchase_quote"),
     (call_script, "script_sod_slavers_buy_slaves_for_player", reg2),
     (call_script, "script_sod_companion_apply_player_action", sod_companion_action_buy_slaves, reg2),
   ]],
]
