DIALOGS = [
[anyone|plyr, "sacrificed_messenger_cancel_2", [(quest_get_slot, ":quest_giver", "qst_incriminate_loyal_commander", slot_quest_giver_troop),
                                                 (call_script, "script_store_troop_name", s3, ":quest_giver"),
      ], "There's a trap set up for you in the town.\
 {s3} ordered me to sacrifice one of my chosen warriors to fool the enemy,\
 but he will just need to find another way.", "sacrificed_messenger_cancel_3", [
     (quest_get_slot, ":quest_giver", "qst_incriminate_loyal_commander", slot_quest_giver_troop),
     (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_current_state, 1),
     (call_script, "script_change_player_relation_with_troop", ":quest_giver", -5),
     (call_script, "script_change_player_honor", 3),
     (call_script, "script_fail_quest", "qst_incriminate_loyal_commander"),
     ]],
]
