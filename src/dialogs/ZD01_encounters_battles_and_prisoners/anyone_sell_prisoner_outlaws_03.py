DIALOGS = [
[anyone, "sell_prisoner_outlaws", [[store_troop_kind_count, 0, "trp_brigand"], [ge, reg(0), 1], [assign, reg(1), reg(0)], [val_mul, reg(1), 30], [assign, reg(2), reg(0)], [val_mul, reg(2), 30]],
   "Well well, you've captured {reg0} brigands. Each one is worth 30 denars, so I'll give you {reg1} for them in total.", "sell_prisoner_outlaws",
   [[call_script, "script_troop_add_gold", "trp_player", reg(1)], [add_xp_to_troop, reg(2)], [remove_member_from_party, "trp_brigand"]]],
]
