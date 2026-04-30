DIALOGS = [
[anyone|plyr, "merchant_talk", [(le, "$talk_context", tc_party_encounter),
                                 (check_quest_active, "qst_raid_caravan_to_start_war"),
                                 (neg|check_quest_concluded, "qst_raid_caravan_to_start_war"),
                                 (quest_slot_eq, "qst_raid_caravan_to_start_war", slot_quest_target_faction, "$g_encountered_party_faction"),
                                 (str_store_faction_name, s17, "$players_kingdom"),
                                 ],
   "You are trespassing in {s17} territory. I am confiscating this caravan and all its goods!", "caravan_start_war_quest_1", []],
]
