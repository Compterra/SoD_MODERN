DIALOGS = [
[anyone|plyr, "lord_pay_debt_2", [(troop_get_slot, ":cur_debt", "$g_talk_troop", slot_troop_player_debt),
                                    (store_troop_gold, ":cur_gold", "trp_player"),
                                    (le, ":cur_debt", ":cur_gold")],
   "That is why I came, {s65}. Here it is, every denar I owe you.", "lord_pay_debt_3_1", [
    (troop_get_slot, ":cur_debt", "$g_talk_troop", slot_troop_player_debt),
    (call_script, "script_sod_player_charge_gold", ":cur_debt"),
    (play_sound, "snd_money_paid"),
    (troop_set_slot, "$g_talk_troop", slot_troop_player_debt, 0)]],
]
