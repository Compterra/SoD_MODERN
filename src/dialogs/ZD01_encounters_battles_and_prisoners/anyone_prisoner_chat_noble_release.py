DIALOGS = [
[anyone,     "prisoner_chat_noble_release", [], "I will not forget this act of Chivalry!", "close_window",
   [
    # remove the troop from prison
    (call_script, "script_remove_troop_from_prison", "$g_talk_troop"),
    (party_remove_prisoners, "p_main_party", "$g_talk_troop", 1),

    # determine how much honor and faction relation change this prisoner is worth
    (try_begin),
      # king
      (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
      (assign, ":honor", 5),
      (assign, ":fac_reln", 15),
    (else_try),
      # other lord
      (assign, ":honor", 2),
      (assign, ":fac_reln", 5),
    (try_end),

    # give the player their honor, faction relation, and lord relation change
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 10),
    (call_script, "script_change_player_honor", ":honor"),
    (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", ":fac_reln" ),
  ]],
]
