DIALOGS = [
[anyone, "lord_hunt_down_fugitive_reward_reject", [],
   "You are a {man/woman} for whom justice is its own reward, eh? Keep the coin, then, {playername}.\
 It is an honourable sentiment, to be true. Regardless, you have my thanks for ridding me of that {s44}.", "lord_pretalk", [

       (troop_get_slot, ":insult_string", "$g_talk_troop", slot_lord_reputation_type),
       (val_add, ":insult_string", "str_lord_insult_default"),
       (str_store_string, s44, ":insult_string"),

       (call_script, "script_change_player_honor", 3),
       (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
       (call_script, "script_end_quest", "qst_hunt_down_fugitive"),
       ]],
]
