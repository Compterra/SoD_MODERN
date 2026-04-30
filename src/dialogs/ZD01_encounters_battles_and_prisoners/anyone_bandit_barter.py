DIALOGS = [
[anyone, "bandit_barter",
   [(store_relation, ":bandit_relation", "fac_player_faction", "$g_encountered_party_faction"),
    (ge, ":bandit_relation", -50),
    (store_mul, "$bandit_tribute", ":bandit_relation", ":bandit_relation"),
    (val_div, "$bandit_tribute", 70),
    (val_add, "$bandit_tribute", 100),
    (val_mul, "$bandit_tribute", 10),
    (assign, reg5, "$bandit_tribute")
    ], "Silver without blood, that's our favourite kind. Pay us {reg5} denars and we'll let you be on your way.", "bandit_barter_2", []],
]
