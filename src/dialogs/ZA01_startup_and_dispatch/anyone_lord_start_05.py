DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_incriminate_loyal_commander"),
                         (check_quest_succeeded, "qst_incriminate_loyal_commander"),
                         (quest_get_slot, ":quest_target_troop", "qst_incriminate_loyal_commander", slot_quest_target_troop),
                         (call_script, "script_store_troop_name", s3, ":quest_target_troop"),
                         (quest_get_slot, reg5, "qst_incriminate_loyal_commander", slot_quest_gold_reward),
                         ],
   "Hah! Our little plot against {s3} worked perfectly, {playername}.\
 The fool has lost one of his most valuable retainers, and we are one step closer to bringing him to his knees.\
 Here, this purse contains {reg5} denars, and I wish you to have it. You deserve every copper.\
 And, need I remind you, there could be much more to come if you've a mind to earn it...", "lord_generic_mission_completed", [
     (call_script, "script_end_quest", "qst_incriminate_loyal_commander"),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 5),
     (call_script, "script_change_player_honor", -10),
     ]],
]
