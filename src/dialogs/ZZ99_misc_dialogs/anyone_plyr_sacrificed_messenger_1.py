DIALOGS = [
[anyone|plyr, "sacrificed_messenger_1", [(quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                                          (str_store_party_name, s1, ":quest_target_center"),
                                          (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
                                          (call_script, "script_store_troop_name", s2, ":quest_object_troop"), ],
   "Take this letter to {s1} and give it to {s2}.", "sacrificed_messenger_2", []],
]
