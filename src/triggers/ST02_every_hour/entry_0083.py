SIMPLE_TRIGGERS = [
(3, [(neg|map_free),
       (check_quest_active, "qst_kill_local_merchant"),
       (quest_slot_eq, "qst_kill_local_merchant", slot_quest_current_state, 0),
       (quest_set_slot, "qst_kill_local_merchant", slot_quest_current_state, 1),
       (rest_for_hours, 0, 0, 0), #stop resting
       (assign, "$auto_enter_town", "$qst_kill_local_merchant_center"),
       (assign, "$quest_auto_menu", "mnu_kill_local_merchant_begin"),
       ]),
]
