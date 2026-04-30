DIALOGS = [
[anyone|plyr, "knight_offer_join_accept_party", [(troop_get_slot, ":companions_party", "$g_talk_troop", slot_troop_leaded_party),
                                       (party_can_join_party, ":companions_party", "p_main_party"),
      ], "Your men may join as well. We need every soldier we can muster.", "knight_join_party_join", []],
]
