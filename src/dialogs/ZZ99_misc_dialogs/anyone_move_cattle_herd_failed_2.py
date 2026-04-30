DIALOGS = [
[anyone, "move_cattle_herd_failed_2", [],
   "Well, it was your responsibility to deliver that herd safely, no matter what.\
 You should know that the owner of the herd demanded to be compensated for his loss, and I had to pay him 1000 denars.\
 So you now owe me that money.", "merchant_ask_for_debts",
   [(assign, "$debt_to_merchants_guild", 1000),
    (call_script, "script_end_quest", "qst_move_cattle_herd"), ]],
]
