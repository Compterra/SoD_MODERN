DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_meet_spy_in_enemy_town"),
                                (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                (str_store_party_name, s13, ":quest_target_center"),
                                (store_faction_of_party, ":quest_target_center_faction", ),
                                (str_store_faction_name, s14, ":quest_target_center_faction"),
                                ],
   "I have a sensitive matter which needs tending to, {playername}, and no trustworthy retainers to take care of it. The fact is that I have a spy in {s13} to keep an eye on things for me, and report anything that might warrant my attention. Every week I send someone to collect the spy's reports and bring them back to me. The job's yours if you wish it.", "lord_mission_told_meet_spy_in_enemy_town",
   [
   ]],
]
