DIALOGS = [
[anyone|plyr, "lord_talk", [(check_quest_active, "qst_deliver_message_to_prisoner_lord"),
                             (quest_slot_eq, "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop, "$g_talk_troop"),
                             (quest_get_slot, ":quest_giver_troop", "qst_deliver_message_to_prisoner_lord", slot_quest_giver_troop),
                             (call_script, "script_store_troop_name", s11, ":quest_giver_troop")],
   "I bring a message from {s11}.", "lord_deliver_message_prisoner",
   [
     #TODO: Add reward
     (call_script, "script_end_quest", "qst_deliver_message_to_prisoner_lord"),
     ]],
]
