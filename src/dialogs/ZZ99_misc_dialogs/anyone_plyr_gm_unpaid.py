DIALOGS = [
[anyone|plyr, "gm_unpaid", [
  (store_troop_gold, ":gold", "trp_player"),
  (ge, ":gold", reg1),
  ], "Here take the money.", "gm_pretalk",[
  (call_script, "script_sod_merc_player_try_settle_debt", "$g_talk_troop_faction"),
  ]],
]
