DIALOGS = [
[anyone, "lord_mission_deal_with_bandits_accepted", [], "Will you do that?\
 Know that, I will be grateful to you. Here is some money for the expenses of your campaign.\
 Make an example of those {s44}s.", "close_window",
   [

    (troop_get_slot, ":insult_string", "$g_talk_troop", slot_lord_reputation_type),
    (val_add, ":insult_string", "str_lord_insult_default"),
    (str_store_string, 44, ":insult_string"),

    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_troop_add_gold", "trp_player", 200),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
    (assign, "$g_leave_encounter", 1),
   ]],
]
