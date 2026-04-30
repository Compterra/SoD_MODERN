DIALOGS = [
[anyone|plyr, "lord_give_money2", [
    (store_troop_gold, ":gold", "trp_player"),
    (ge, ":gold", 10000),
  ], "Here, take this 10000 gold", "lord_pretalk", [
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 4),
    (troop_remove_gold, "trp_player", 10000),
    (play_sound, "snd_money_paid"),
	(troop_get_slot, ":cur_gold", "$g_talk_troop", slot_troop_wealth),
	(val_add, ":cur_gold", 10000),
	(troop_set_slot, "$g_talk_troop", slot_troop_wealth, ":cur_gold"),
  ]],
]
