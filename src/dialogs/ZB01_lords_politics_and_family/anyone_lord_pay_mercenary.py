DIALOGS = [
[anyone, "lord_pay_mercenary", [(assign, reg8, "$mercenary_service_accumulated_pay")],
   "Hmm, let me see... According to my ledgers, we owe you {reg8} denars for your work. Here you are.", "lord_pay_mercenary_2",
   [(call_script, "script_merc_collect_service_pay")]],
]
