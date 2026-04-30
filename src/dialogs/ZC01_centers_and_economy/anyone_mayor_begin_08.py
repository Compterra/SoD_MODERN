DIALOGS = [
[anyone, "mayor_begin", [(ge, "$debt_to_merchants_guild", 50)],
   "According to my accounts, you owe the merchants guild {reg1} denars.\
 I'd better collect that now.", "merchant_ask_for_debts", [(assign, reg(1), "$debt_to_merchants_guild")]],
]
