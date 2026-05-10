DIALOGS = [
[anyone, "start", [(store_partner_quest, ":lords_quest"),
                         (this_or_next|eq, ":lords_quest", "qst_black_army_collect_debt"),
                         (this_or_next|eq, ":lords_quest", "qst_conquistadors_collect_debt"),
						 (eq, ":lords_quest", "qst_slavers_collect_debt"),
                         (quest_slot_eq, ":lords_quest", slot_quest_current_state, 1),
                         (quest_get_slot, ":target_troop", ":lords_quest", slot_quest_target_troop),
                         (call_script, "script_store_troop_name", s7, ":target_troop"),
                         (quest_get_slot, ":total_collected", ":lords_quest", slot_quest_target_amount),
                         (store_div, reg3, ":total_collected", 5),
                         (store_sub, reg4, ":total_collected", reg3)],
   "I'm told that you've collected the money owed me from {s7}. Good, it's past time I had it back.\
 I believe I promised to give you one-fifth of it all, eh?\
 Well, that makes {reg3} denars, so if you give me my share -- that's {reg4} denars -- you can keep the rest.", "gm_collect_debt_completed", []],
]
