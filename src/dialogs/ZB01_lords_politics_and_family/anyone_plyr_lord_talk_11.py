DIALOGS = [
[anyone|plyr, "lord_talk", [(check_quest_active, "qst_deliver_message_to_enemy_lord"),
                            (quest_get_slot, ":quest_target_troop", "qst_deliver_message_to_enemy_lord", slot_quest_target_troop),
                            (eq, "$g_talk_troop", ":quest_target_troop"),
                            (quest_get_slot, ":quest_giver_troop", "qst_deliver_message_to_enemy_lord", slot_quest_giver_troop),
                            (call_script, "script_store_troop_name", s9, ":quest_giver_troop")],
   "I bring a message from {s9}.", "lord_message_delivered_enemy",
   []],
]
