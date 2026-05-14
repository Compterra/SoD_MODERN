DIALOGS = [
[anyone|plyr, "seneschal_talk", [(store_relation, ":cur_rel", "fac_player_supporters_faction", "$g_encountered_party_faction"),
                                  (ge, ":cur_rel", 0), ],
   "Bring me what the household knows about a name.", "seneschal_ask_about_someone", []],
]
