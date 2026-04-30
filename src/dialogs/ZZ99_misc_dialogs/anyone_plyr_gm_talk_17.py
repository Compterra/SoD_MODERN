DIALOGS = [
[anyone|plyr, "gm_talk", [
   (this_or_next|eq,"$g_talk_troop", slavers_rep),
   (eq,"$g_talk_troop", slavers_guild_master),
   (store_num_regular_prisoners, reg0), 
   (ge, reg0, 1)
   ], "I've brought you some prisoners. Would you like a look?", "gm_talk_sell_prisoners", []],
]
