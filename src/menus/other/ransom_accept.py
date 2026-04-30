MENUS = [
(
    "enemy_offer_ransom_for_prisoner", 0,
    "{s2} offers you a sum of {reg12} denars in silver if you are willing to sell him {s1}.",
    "none",
    [(call_script, "script_calculate_ransom_amount_for_troop", "$g_ransom_offer_troop"),
     (assign, reg12, reg0),
     (call_script, "script_store_troop_name", s1, "$g_ransom_offer_troop"),
     (store_troop_faction, ":faction_no", "$g_ransom_offer_troop"),
     (str_store_faction_name, s2, ":faction_no"),
     ],
    [
      ("ransom_accept", [], "Accept the offer.",
       [(troop_add_gold, "trp_player", reg12),
        (party_remove_prisoners, "$g_ransom_offer_party", "$g_ransom_offer_troop", 1),
        #(troop_set_slot, "$g_ransom_offer_troop", slot_troop_is_prisoner, 0),
        (call_script, "script_remove_troop_from_prison", "$g_ransom_offer_troop"),
        (change_screen_return),
        ]),
      ("ransom_reject", [], "Reject the offer.",
       [
        (call_script, "script_change_player_relation_with_troop", "$g_ransom_offer_troop", -4),
        (try_begin),
        (store_troop_faction, ":faction_no", "$g_ransom_offer_troop"),
        (neg|eq, ":faction_no", "fac_kingdom_6"),
        (call_script, "script_change_player_honor", -1),
        (try_end),
        (assign, "$g_ransom_offer_rejected", 1),
        (change_screen_return),
        ]),
    ]
  ),
]
