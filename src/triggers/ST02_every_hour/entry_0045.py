SIMPLE_TRIGGERS = [
(3,
   [
    (assign, "$g_center_taken_by_player_faction", -1),
    (try_for_range, ":center_no", centers_begin, centers_end),
      (eq, "$g_center_taken_by_player_faction", -1),
      (store_faction_of_party, ":center_faction", ":center_no"),
      (eq, ":center_faction", "fac_player_supporters_faction"),
      (this_or_next|party_slot_eq, ":center_no", slot_town_lord, stl_reserved_for_player),
      (this_or_next|party_slot_eq, ":center_no", slot_town_lord, stl_unassigned),
      (party_slot_eq, ":center_no", slot_town_lord, stl_rejected_by_player),
      (assign, "$g_center_taken_by_player_faction", ":center_no"),
    (try_end),
    (ge, "$g_center_taken_by_player_faction", 0),
    (faction_get_slot, ":leader", "fac_player_supporters_faction", slot_faction_leader),
    (try_begin),
      (eq, ":leader", "trp_player"),
      #MORDACHAI - DEBUG - this happens if player takes a center, but it isn't assigned to anyone (yet)
      #MORDACHAI - DEBUG - this should no longer occur, as conquests are immediately fully assigned to the player now (see mnu_castle_taken)
      (str_store_party_name_link, s2, "$g_center_taken_by_player_faction"),
      (party_get_slot, reg1, ":center_no", slot_town_lord),
      (display_message, "@ERROR {s2}'s slot_town_lord = {reg1}", red),
    (else_try),
      (start_map_conversation, ":leader"),
    (try_end),
    ]),
]
