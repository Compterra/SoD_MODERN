DIALOGS = [
[trp_ramun_the_slave_trader, "ramun_sell_prisoners", [],
  "Let me see what you have...", "ramun_sell_prisoners_2",
   [
     (call_script, "script_sod_slavers_apply_player_action", sod_slaver_action_trade_prisoners, 2),
     (call_script, "script_sod_companion_apply_player_action", sod_companion_action_sell_prisoners, 2),
     [change_screen_trade_prisoners],
   ]],
]
