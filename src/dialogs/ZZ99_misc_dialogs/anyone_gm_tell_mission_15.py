DIALOGS = [
[anyone, "gm_tell_mission", [(eq, "$random_quest_no", "qst_conquistadors_deliver_horses")],
   "While we managed to carry on our duty so far, our lack of cavalry is becoming a pressing issue.  I was planning to expand the Lancer branch of the company, but I want only the best breeds in the land, and I don't trust the local stable masters too much, because they are just as suspicious towards us like the other merchants and might cheat us.  I trust your eyes are better at judging the local steeds than mine, because due to some gossip, I'm particularly interested in a certain breed.  If you could visit the stables and bring us {reg5?{reg5}:a} {s13} mount{reg5?s:}, we would be very thankful and eager to pay well for them.", "gm_tell_deliver_grain_mission_3",
   [
	 (quest_get_slot, ":quest_target_item", "$random_quest_no", slot_quest_target_item),
     (quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount),
	 (str_store_item_name_plural, s13, ":quest_target_item"),
   ]],
]
