DIALOGS = [
[anyone, "sell_prisoner_outlaws", [[store_troop_kind_count, 0, "trp_bandit"], [ge, reg(0), 1], [assign, reg(1), reg(0)], [val_mul, reg(1), 20], [assign, reg(2), reg(0)], [val_mul, reg(2), 20]],
   "Let me see. You've brought {reg0} bandits, so 20 denars for each comes up to {reg1} denars.", "sell_prisoner_outlaws",
   [[call_script, "script_troop_add_gold", "trp_player", reg(1)], [add_xp_to_troop, reg(2)], [remove_member_from_party, "trp_bandit"]]],
]
