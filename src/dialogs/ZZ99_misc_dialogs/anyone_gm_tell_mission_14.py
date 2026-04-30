DIALOGS = [
[anyone, "gm_tell_mission", [(eq, "$random_quest_no", "qst_conquistadors_deliver_grain")],
   "We, the Conquistadors use only first-grade materials to forge our equipment, but even after a decent period of service to the Kingdom of Vaegirs many merchants are still rather suspicious towards us and charge the price of their wares pretty high, and I'm growing tired of their unfair methods.  Since you're probably more accustomed to the local conditions than me, the merchants are likely to sell their ware for less to you.  So, getting to the point, if you would purchase {reg5} loads of pure Iron and bring it to our fort, we'd be willing to pay slightly more for it than the original price - both you and us would benefit from it.  Fair trade, unlike theirs.  So, are you interested?", "gm_tell_deliver_grain_mission_3",
   [
	 (quest_get_slot, ":quest_target_item", "$random_quest_no", slot_quest_target_item),
     (quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount),
	 (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
	 (str_store_item_name_plural, s13, ":quest_target_item"),
   ]],
]
