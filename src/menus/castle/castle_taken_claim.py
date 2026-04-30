MENUS = [
(
    "castle_taken_2", mnf_disable_all_keys,
    "{s3} has fallen to your troops, and you now have full control of the castle. It is time to send word to {s9} about your victory. {s5}",
    "none",
    [
      (str_store_party_name, s3, "$g_encountered_party"),
      (str_clear, s5),
      (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
      (call_script, "script_store_troop_name", s9, ":faction_leader"),
      (try_begin),
        (eq, "$player_has_homage", 0),
        (assign, reg8, 0),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", spt_town),
          (assign, reg8, 1),
        (try_end),
        (str_store_string, s5, "@However, since you are not a sworn {man/follower} of {s9}, there is no chance he would recognize you as the {lord/lady} of this {reg8?town:castle}."),
      (try_end),
    ],
    [
      ("castle_taken_claim", [(eq, "$player_has_homage", 1)], "Request that {s3} be awarded to you.",
       [
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, "trp_player"),
        (assign, "$g_castle_requested_by_player", "$current_town"),
        (assign, "$auto_enter_town", "$g_encountered_party"),
        (change_screen_return),
        ]),
      ("castle_taken_no_claim", [], "Ask no rewards.",
       [
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, -1),
        (assign, "$auto_enter_town", "$g_encountered_party"),
        (change_screen_return),
       ]),
    ],
  ),
]
