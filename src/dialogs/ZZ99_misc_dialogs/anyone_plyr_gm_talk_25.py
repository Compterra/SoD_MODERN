DIALOGS = [
[anyone|plyr, "gm_talk", [
   (neq, "$g_rep", "$g_talk_troop"),
   (ge, "$g_talk_troop_faction_relation", 40),
   (assign, ":has_ties", 0),
   (try_begin),
     (faction_slot_eq, "fac_player_faction", slot_faction_merc_pact, "$g_talk_troop_faction"),
     (assign, ":has_ties", 1),
   (else_try),
     (try_for_parties, ":cur_party"),
       (party_slot_eq, ":cur_party", slot_party_type, spt_player_mercenaries),
       (party_slot_eq, ":cur_party", slot_party_boss, "trp_player"),
       (party_slot_eq, ":cur_party", slot_party_orginal_faction, "$g_talk_troop_faction"),
       (assign, ":has_ties", 1),
     (try_end),
   (try_end),
   (eq, ":has_ties", 1),
   ], "As a trusted partner, can your guild extend us a favor?", "gm_trusted_favor",[]],
]
