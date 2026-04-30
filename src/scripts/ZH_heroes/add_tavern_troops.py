SCRIPTS = [
("add_tavern_troops",
                      [
                        (try_for_range, reg(2), merc_parties_begin, merc_parties_end),
                          (store_party_size, reg(6), reg(2)),
                          (lt, reg(6), 30), #never have many more than 20 troops in the tavern
                          (store_random, reg(7), 8),
                          (party_add_members, reg(2), "trp_townsman", reg(7)),
                          (store_random, reg(8), 5),
                          (party_add_members, reg(2), "trp_refugee", reg(8)),
                          (store_random, reg(9), 5),
                          (party_add_members, reg(2), "trp_manhunter", reg(9)),
                        (try_end),
                    ]),
]
