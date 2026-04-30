DIALOGS = [
[anyone, "event_triggered",
    [
      # this applies only if we're talking to the lord that is offering his/her allegience (see simple trigger #44 Respawn hero party after kingdom hero is released from captivity)
      (eq, "$g_sod_lord_offers_allegience", "$g_talk_troop"),
      (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),

      # s41 = player's empire
      (str_store_faction_name, 41, "fac_player_supporters_faction"),
      # s42 = lord's name
      (call_script, "script_store_troop_name", 42, "$g_sod_lord_offers_allegience"),

      # set reg0 = is friend
      (try_begin),
        (ge, "$g_talk_troop_relation", 20),
        (assign, reg0, 1),
      (else_try),
        (assign, reg0, 0),
      (try_end),
    ],
    "{reg0?My friend, :}{Lord/Lady} {playername}", "loa_start", []],
]
