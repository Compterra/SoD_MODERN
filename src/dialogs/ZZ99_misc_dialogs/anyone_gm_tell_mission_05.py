DIALOGS = [
[anyone, "gm_tell_mission", [(eq, "$random_quest_no", "qst_serpent_host_raid_caravan"),
                                (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
                                (str_store_faction_name_link, s13, ":quest_target_faction")],
   "The Rhodoks often charge us with harassing {s13} caravans. I appreciate their trust towards us, but too many times I end up realizing that I have to send out too many good fighters for dealing with such an insignificant task, while I could make better use of them elsewhere. I would be glad if you, young spirit, were willing to take this mission over for this time. You may keep whatever supplies and riches you find among the wrecks, just make sure that when you're done report back to me. Does the offer sound well for you ?", "gm_mission_told_raid_caravan",
   [
   ]],
]
