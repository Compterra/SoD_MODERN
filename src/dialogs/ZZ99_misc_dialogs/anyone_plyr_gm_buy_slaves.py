DIALOGS = [
[anyone|plyr, "gm_talk",
   [
     (this_or_next|eq, "$g_talk_troop", slavers_rep),
     (eq, "$g_talk_troop", slavers_guild_master),
     (call_script, "script_sod_slavers_store_slave_purchase_quote"),
     (gt, reg2, 0),
   ],
   "I want to buy slaves for my party.", "sod_slaver_buy_slaves_quote", []],
]
