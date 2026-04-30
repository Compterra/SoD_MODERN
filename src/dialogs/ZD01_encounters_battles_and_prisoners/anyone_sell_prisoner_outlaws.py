DIALOGS = [
[anyone, "sell_prisoner_outlaws", [[store_troop_kind_count, 0, "trp_looter"], [ge, reg(0), 1], [assign, reg(1), reg(0)], [val_mul, reg(1), 10], [val_mul, reg(2), reg(0)], [val_mul, reg(2), 10]],
   "Hmmm. 10 denars for each looter makes {reg1} denars for all {reg0} of them.", "sell_prisoner_outlaws",
   [[call_script, "script_troop_add_gold", "trp_player", reg(1)], [add_xp_to_troop, reg(2)], [remove_member_from_party, "trp_looter"]]],
]
