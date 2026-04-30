DIALOGS = [
[anyone, "tavernkeeper_buy_peasants",
   [
       (store_encountered_party, reg(3)),
       (store_faction_of_party, reg(4), reg(3)),
       (store_relation, reg(5), "fac_player_supporters_faction", reg(4)),
       (lt, reg(5), -3),
    ], "I don't think anyone from this town will follow somebody like you. Try your luck elsewhere.", "tavernkeeper_buy_peasants_2", []],
]
