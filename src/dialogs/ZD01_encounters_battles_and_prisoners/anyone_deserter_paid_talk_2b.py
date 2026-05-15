DIALOGS = [
[anyone, "deserter_paid_talk_2b", [], "What nonsense are you talking about? You want trouble? You got it.", "close_window", [
       (party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, 0),
       (party_ignore_player, "$g_encountered_party", 0),
       (assign, "$g_enemy_party", "$g_encountered_party"),
       (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
       (encounter_attack),
    ]],
]
