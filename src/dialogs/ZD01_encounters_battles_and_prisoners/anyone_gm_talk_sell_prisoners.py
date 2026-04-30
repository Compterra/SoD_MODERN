DIALOGS = [
[anyone, "gm_talk_sell_prisoners", [
   (this_or_next|eq, "$g_talk_troop", slavers_guild_master),
   (eq, "$g_talk_troop", slavers_rep),
  ],
  "Let me see what you have. Live stock, troublemakers, deserters - we take them all.", "gm_talk_sell_prisoners_2",
   [(change_screen_trade_prisoners)]],
[anyone, "gm_talk_sell_prisoners", [],
  "Let me see what you have...", "gm_talk_sell_prisoners_2",
   [(change_screen_trade_prisoners)]],
]
