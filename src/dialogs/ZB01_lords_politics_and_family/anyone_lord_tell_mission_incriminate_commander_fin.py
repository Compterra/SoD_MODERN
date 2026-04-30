DIALOGS = [
[anyone, "lord_tell_mission_incriminate_commander_fin", [], "I can't tell you how pleased I am to hear that,\
 {playername}. You are removing one of the greatest obstacles in my path.\
 Here is the letter, as well as 300 denars for your expenses.\
 Remember, there'll be more once you succeed. Much, much more...", "lord_pretalk",
   [
       (quest_get_slot, ":quest_target_troop", "qst_incriminate_loyal_commander", slot_quest_target_troop),
       (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
       (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
       (call_script, "script_troop_add_gold", "trp_player", 300),
       (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
       (call_script, "script_store_troop_name_link", s11, "$g_talk_troop"),
       (call_script, "script_store_troop_name_link", s13, ":quest_target_troop"),
       (str_store_party_name_link, s14, ":quest_target_center"),
       (str_store_troop_name_plural, s15, "$incriminate_quest_sacrificed_troop"),
       (call_script, "script_store_troop_name_link", s16, ":quest_object_troop"),
       (setup_quest_text, "$random_quest_no"),
       (str_store_string, s2, "@{s11} gave you a fake letter to fool {s13} into banishing his vassal {s16}.\
 You are to go near {s14}, give the letter to one of your {s15} and send him into the town as a messenger,\
 believing his orders to be genuine."),
       (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],
]
