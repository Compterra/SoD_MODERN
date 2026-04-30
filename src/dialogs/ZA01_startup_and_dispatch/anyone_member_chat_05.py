DIALOGS = [
[anyone, "member_chat", [(check_quest_active, "qst_incriminate_loyal_commander"),
                          (quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_current_state, 0),
                          (store_conversation_troop, "$g_talk_troop"),
                          (eq, "$g_talk_troop", "$incriminate_quest_sacrificed_troop"),
                          (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
                          (store_distance_to_party_from_party, ":distance", "p_main_party", ":quest_target_center"),
                          (lt, ":distance", 10),
                          ], "Yes {sir/madam}?", "sacrificed_messenger_1", []],
]
