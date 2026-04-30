DIALOGS = [
[anyone     , "loa_swear_oath_done", [], "Thank you, my liege.  I will serve you honorably.^^As soon as I can arrange, I shall return with my most loyal followers to do your will.", "loa_swear_oath_finish",
    [
      # accepted - defect the lord to player's faction (after the troop joins our faction, he should spawn in a party shortly thereafter)
      (troop_set_slot, "$g_talk_troop", slot_lord_allegience_offered, lao_accepted),
      (troop_set_slot, "$g_talk_troop", slot_troop_change_to_faction, "fac_player_supporters_faction"),
      (store_random_in_range, reg0, 1, 11),
      (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", reg0),

      # reset the lord's cash to minimal.  he shouldn't be running around with a fortune!
      (store_troop_gold, ":gold", "$g_talk_troop"),
      (troop_remove_gold, ":gold", "$g_talk_troop"),
      (troop_add_gold, "$g_talk_troop", recruited_lord_starting_funds),

      (assign, "$g_sod_lord_offers_allegience", 0),
    ]
  ],
]
