DIALOGS = [
[anyone, "lord_collect_taxes_half_success", [(quest_get_slot, ":gold_reward", "qst_collect_taxes", slot_quest_gold_reward),
                                         (val_mul, ":gold_reward", 95),
                                         (val_div, ":gold_reward", 100),
                                         (assign, reg20, ":gold_reward")],
   "What?! Is this some scheme of yours, {playername}? That's less than half the taxes I'm owed!\
 You have let them get away with murder as well as my money. What a farce!\
 You can forget the money I promised you, I'm taking {reg20} denars from what you collected,\
 and you're lucky I'm leaving you a few coins for honour's sake.", "lord_pretalk",
   [(call_script, "script_sod_player_charge_gold", reg20),
    (play_sound, "snd_money_paid"),
    (quest_set_slot, "qst_collect_taxes", slot_quest_gold_reward, 0),
    (call_script, "script_end_quest", "qst_collect_taxes"),
    ]],
]
