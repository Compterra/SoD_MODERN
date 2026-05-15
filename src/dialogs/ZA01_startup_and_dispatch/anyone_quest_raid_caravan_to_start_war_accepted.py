DIALOGS = [
[anyone, "quest_raid_caravan_to_start_war_accepted", [
     (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
     (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
     (str_store_faction_name_link, s68, ":quest_target_faction"),
     (assign, reg13, ":quest_target_amount"),
   ], "Very good!\
 Now, don't forget that you must capture and loot at least {reg13} caravans to make sure that those fools in {s68} get really infuriated.\
 Once you do that, return to me and make sure you are not captured by their patrols.\
 If they catch you, our plan will fail without a doubt and you will be facing a long time in prisons.\
 Now, good luck and good hunting to you.", "close_window",
   [
     (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
     (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (str_store_faction_name_link, s13, ":quest_target_faction"),
     (assign, reg13, ":quest_target_amount"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to capture and loot {reg13} caravans so as to provoke a war with {s13}."),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 5),
     (assign, "$g_leave_encounter", 1),
    ]],
]
