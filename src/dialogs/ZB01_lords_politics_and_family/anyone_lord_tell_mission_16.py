DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_incriminate_loyal_commander"),
                                (quest_get_slot, ":quest_target_troop", "qst_incriminate_loyal_commander", slot_quest_target_troop),
                                (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
                                (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                                (call_script, "script_store_troop_name_link", s13, ":quest_target_troop"),
                                (str_store_party_name_link, s14, ":quest_target_center"),
                                (call_script, "script_store_troop_name_link", s15, ":quest_object_troop"),
                                ],
 "I tell you, that blubbering fool {s13} is not fit to rule {s14}.\
 God knows he would be divested of his lands in an instant were it not for one of his loyal vassals, {s15}.\
 As long as he has his vassal aiding him, it will be a difficult job beating him.\
 So I need to get {s15} out of the picture, and I have a plan just to do that...\
 With your help, naturally.", "lord_tell_mission_incriminate_commander", []],
]
