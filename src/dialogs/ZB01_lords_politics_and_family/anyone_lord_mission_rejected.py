DIALOGS = [
[anyone, "lord_mission_rejected", [], "Is that so? Well, I suppose you're just not up to the task.\
 I shall have to look for somebody with more mettle.", "close_window",
   [(assign, "$g_leave_encounter", 1),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (try_begin),
      (quest_slot_eq, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 0),
      (quest_set_slot, "$random_quest_no", slot_quest_dont_give_again_remaining_days, 1),
    (try_end),
    (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    ]],
]
