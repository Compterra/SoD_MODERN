DIALOGS = [
[anyone, "lord_mission_deliver_message_rejected_rudely_3", [], "All right. I will remember that.", "close_window", [
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -4),
    (quest_set_slot, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 150),
    (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    (assign, "$g_leave_encounter", 1),
      ]],
]
