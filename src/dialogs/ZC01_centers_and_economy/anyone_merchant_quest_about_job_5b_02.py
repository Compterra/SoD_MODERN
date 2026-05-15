DIALOGS = [
[anyone, "lost_kidnapped_girl_debt", [(gt, "$g_sod_lost_rescue_repayment_amount", 0)],
   "Then it stays on your account. Bring the money when you have it.",
   "close_window", [(val_add, "$debt_to_merchants_guild", "$g_sod_lost_rescue_repayment_amount"),
                   (assign, "$g_sod_lost_rescue_repayment_amount", 0),
                   ]],
]
