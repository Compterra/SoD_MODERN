DIALOGS = [
[anyone|plyr, "lord_gm_message_delivered1", [
                             (quest_get_slot, ":quest_giver_troop", "$g_cur_deliver_quest", slot_quest_giver_troop),
                             (call_script, "script_store_troop_name", s9, ":quest_giver_troop")],
   "From {s9}.", "lord_gm_message_delivered",
   []],
]
