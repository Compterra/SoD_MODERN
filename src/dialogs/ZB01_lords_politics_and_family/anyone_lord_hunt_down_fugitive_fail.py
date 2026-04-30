DIALOGS = [
[anyone, "lord_hunt_down_fugitive_fail", [],
   "It is a sad day when that {s44} manages to avoid the hand of justice yet again.\
 I thought you would be able to do this, {playername}. Clearly I was wrong.", "lord_pretalk",
   [
    (troop_get_slot, ":insult_string", "$g_talk_troop", slot_lord_reputation_type),
    (val_add, ":insult_string", "str_lord_insult_default"),
    (str_store_string, 44, ":insult_string"),

    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (call_script, "script_end_quest", "qst_hunt_down_fugitive"),
    ]],
]
