DIALOGS = [
[anyone|plyr, "bandit_meet", [], "Your luck has run out, wretch. Prepare to die!", "bandit_attack",
   [(store_relation, ":bandit_relation", "fac_player_faction", "$g_encountered_party_faction"),
    (val_sub, ":bandit_relation", 3),
    (val_max, ":bandit_relation", -100),
    (set_relation, "fac_player_faction", "$g_encountered_party_faction", ":bandit_relation"),
    (party_ignore_player, "$g_encountered_party", 0),
    (party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, 0),
    ]],
]
