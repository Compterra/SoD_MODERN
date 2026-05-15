DIALOGS = [
[anyone|plyr, "seneschal_talk",
   [(store_relation, ":cur_rel", "fac_player_supporters_faction", "$g_encountered_party_faction"),
    (ge, ":cur_rel", 0),
    (is_between, "$g_encountered_party", centers_begin, centers_end)],
   "Open the household health rolls.", "seneschal_public_health", []],
]
