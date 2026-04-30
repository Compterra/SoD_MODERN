DIALOGS = [
[anyone|plyr, "runaway_slave_reconsider", [], "I have changed my mind. You must back to your cages!", "runaway_slave_go_back",
   [(party_set_slot, "$g_encountered_party", slot_town_castle, 0),
    (call_script, "script_change_player_honor", -2),
	(val_sub, "$qst_bring_back_runaway_slaves_num_parties_fleed", 1),
	]],
]
