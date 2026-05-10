DIALOGS = [
[anyone|plyr, "deserter_talk", [
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (ge, ":enemy_size", 6),
], "Send your captain forward. One blade can spare the rest of your men.", "hostile_leader_duel_challenge", []],
]
