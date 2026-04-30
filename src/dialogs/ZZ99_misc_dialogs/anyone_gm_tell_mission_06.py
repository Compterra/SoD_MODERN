DIALOGS = [
[anyone, "gm_tell_mission", [(eq, "$random_quest_no", "qst_serpent_host_free_spy"),
                                (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                (str_store_party_name_link, s13, ":quest_target_center")],
   "There's a man I sent out to {s13} to spy around, but word came that he was caught and his captors now demand a ransom for him. Going out to negotiate would be a source of shame. Ramsacking a whole village for a single man is unreasonable. But sending a 'third person' like you would have no diplomatic weight. However, once you're there, you'll have to make a decision to either bribe the guards keeping our spy captive or fight the town watch and free my subject from his cell. Whichever you choose, afterwards you'll have to escort him back to the headquarters. Make sure he arrives safe and sound - if you do, you may be sure to receive a fitting reward.", "gm_mission_told_free_spy",
   [
   ]],
]
