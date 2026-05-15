DIALOGS = [
[anyone, "gm_tell_mission", [(eq, "$random_quest_no", "qst_serpent_host_free_spy"),
                                (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                (str_store_party_name_link, s13, ":quest_target_center")],
   "One of my spies was taken near {s13}. The militia want ransom; if I send soldiers, it becomes politics. Take the money, judge the captors yourself, and bring him back to Sukbathar alive. Pay them if that buys silence. Cut him out if it does not.", "gm_mission_told_free_spy",
   [
   ]],
]
