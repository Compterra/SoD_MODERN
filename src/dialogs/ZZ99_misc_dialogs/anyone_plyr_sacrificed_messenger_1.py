DIALOGS = [
[anyone|plyr, "sacrificed_messenger_1", [(check_quest_active, "qst_incriminate_loyal_commander"),
                                          (neg|check_quest_concluded, "qst_incriminate_loyal_commander"),
                                          (quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_current_state, 0),
                                          (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                                          (party_is_active, ":quest_target_center"),
                                          (str_store_party_name, s1, ":quest_target_center"),
                                          (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
                                          (call_script, "script_store_troop_name", s2, ":quest_object_troop"), ],
   "Take this letter to {s1}. Put it in {s2}'s hand, and speak to no one else.", "sacrificed_messenger_2", []],
]
