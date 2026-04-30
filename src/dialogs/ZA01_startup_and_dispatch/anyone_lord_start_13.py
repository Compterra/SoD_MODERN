DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_kill_local_merchant"),
                         (check_quest_succeeded, "qst_kill_local_merchant"),
                         (quest_slot_eq, "qst_kill_local_merchant", slot_quest_current_state, 2)],
   "You! Do you have sawdust between your ears? Did you think that when I said to kill the merchant, "\
   "I meant you to have a nice chat with him and then let him go?! What possessed you?", "lord_kill_local_merchant_let_go", []],
]
