DIALOGS = [
[anyone, "lord_message_delivered_enemy", [], "Oh? Let me see that...\
 Hmmm. It was good of you to bring me this, {playername}. Take my seal as proof that I've received it,\
 with my thanks.", "close_window", [
     (call_script, "script_end_quest", "qst_deliver_message_to_enemy_lord"),
     (quest_get_slot, ":quest_giver", "qst_deliver_message_to_enemy_lord", slot_quest_giver_troop),
     (call_script, "script_change_player_relation_with_troop", ":quest_giver", 3),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter", 1),
     ]],
]
