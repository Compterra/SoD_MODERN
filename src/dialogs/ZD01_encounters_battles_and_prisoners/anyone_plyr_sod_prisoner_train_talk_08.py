DIALOGS = [
[anyone|plyr, "sod_prisoner_train_talk", [
    (party_get_slot, ":purpose", "$g_encountered_party", slot_party_sod_prisoner_purpose),
    (this_or_next|eq, ":purpose", sod_prisoner_train_purpose_slaver_market),
    (eq, ":purpose", sod_prisoner_train_purpose_labor),
  ], "These people are not cargo. I am freeing them.", "close_window", [
    (call_script, "script_sod_player_accept_prisoner_train_quest_hook", "$g_encountered_party", 3),
    (assign, "$g_enemy_party", "$g_encountered_party"),
    (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
    (encounter_attack),
  ]],
]
