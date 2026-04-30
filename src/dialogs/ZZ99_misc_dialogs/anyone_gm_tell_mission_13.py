DIALOGS = [
[anyone, "gm_tell_mission", [(eq, "$random_quest_no", "qst_elephant_guard_deliver_grain")],
   "We are still in the process to adapt to the northern environment and weather. Our Khergit friends have helped us much, but alas, most recently we've ran out of {s13}. These are necessary for maintaining life in our village, but are hard to acquire on our own and caravans rarely pass by due to steppe bandits.", "gm_tell_deliver_grain_mission",
   [
	 (quest_get_slot, ":quest_target_item", "$random_quest_no", slot_quest_target_item),
     (quest_get_slot, reg5, "$random_quest_no", slot_quest_target_amount),
	 (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
	 (str_store_item_name_plural, s13, ":quest_target_item"),
   ]],
]
