SIMPLE_TRIGGERS = [
(0,
   [
      (eq, "$g_player_is_captive", 1),
      (gt, "$capturer_party", 0),
      (party_is_active, "$capturer_party"),
      (party_relocate_near_party, "p_main_party", "$capturer_party", 0),
    ]),
]
