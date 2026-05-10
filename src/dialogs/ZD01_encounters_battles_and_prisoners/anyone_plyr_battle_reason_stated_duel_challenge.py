DIALOGS = [
[anyone|plyr, "battle_reason_stated", [
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (ge, ":enemy_size", 6),
], "Send your captain forward. One blade can settle whether this road is worth dying on.", "hostile_leader_duel_challenge", []],
]
