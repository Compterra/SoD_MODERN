DIALOGS = [
[anyone, "lord_mission_tell_raid_caravan_to_start_war_2", [(quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
                                                            (str_store_faction_name_link, s13, ":quest_target_faction")],
   "Ah, 'tis good to hear someone who understands!\
 As a matter of fact, there is something we can do, {playername}. A little bit of provocation.\
 The dogs in {s13} are very fond of their merchant caravans, and rely on them overmuch.\
 If one of our war parties managed to enter their territory and pillage some of their caravans,\
 they would have ample cause to declare war on our kingdom.\
 And then, well, even the cowards among us must rise to defend themselves.\
 So what do you say? Are you interested?", "lord_mission_tell_raid_caravan_to_start_war_3", []],
]
