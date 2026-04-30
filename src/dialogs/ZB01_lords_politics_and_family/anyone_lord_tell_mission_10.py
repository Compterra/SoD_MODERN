DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_raid_caravan_to_start_war"),
                                (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
                                (str_store_faction_name_link, s13, ":quest_target_faction")],
   "This peace with {s13} ill suits me, {playername}. We've let those swine have their way for far too long.\
 Now they get stronger with each passing and their arrogance knows no bounds.\
 I say, we must wage war on them before it's too late!\
 Unfortunately, some of the bleeding hearts among our realm's lords are blocking a possible declaration of war.\
 Witless cowards with no stomach for blood.", "lord_mission_told_raid_caravan_to_start_war",
   [
   ]],
]
