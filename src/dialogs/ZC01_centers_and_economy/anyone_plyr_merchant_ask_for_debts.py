DIALOGS = [
[anyone|plyr, "merchant_ask_for_debts", [[store_troop_gold, reg(5), "trp_player"], [ge, reg(5), "$debt_to_merchants_guild"]],
   "Here is what I owe. Let the account breathe again.", "merchant_debts_paid", [
    [call_script, "script_sod_player_charge_gold", "$debt_to_merchants_guild"],
    (play_sound, "snd_money_paid"),
    [assign, "$debt_to_merchants_guild", 0]]],
]
