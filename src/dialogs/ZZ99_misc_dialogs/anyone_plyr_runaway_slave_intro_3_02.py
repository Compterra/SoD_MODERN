DIALOGS = [
[anyone|plyr, "runaway_slave_intro_3", [], "Well, maybe you are right. All right then. If anyone asks, I haven't seen you.", "runaway_slave_let_go",
   [(party_set_slot, "$g_encountered_party", slot_town_castle, 1),
   (val_add, "$qst_bring_back_runaway_slaves_num_parties_fleed", 1),
   (call_script, "script_change_player_honor", 5)]],
]
