DIALOGS = [
[anyone, "village_elder_ask_enemies",
   [
     (assign, ":give_report", 0),
     (party_get_slot, ":original_faction", "$g_encountered_party", slot_center_original_faction),
     (store_relation, ":original_faction_relation", ":original_faction", "fac_player_supporters_faction"),
     (try_begin),
       (gt, ":original_faction_relation", 0),
       (party_slot_ge, "$g_encountered_party", slot_center_player_relation, 0),
       (assign, ":give_report", 1),
     (else_try),
       (party_slot_ge, "$g_encountered_party", slot_center_player_relation, 30),
       (assign, ":give_report", 1),
     (try_end),
     (eq, ":give_report", 0),
     ],
   "I am sorry, {sir/madam}. We have neither seen nor heard of any war parties in this area.", "village_elder_pretalk",
   []],
]
