DIALOGS = [
[anyone, "event_triggered",
   [
     (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "$g_talk_troop"),
     (is_between, "$g_center_taken_by_player_faction", centers_begin, centers_end),
     (str_store_party_name, s68, "$g_center_taken_by_player_faction"),
     ],
   "{s68} is not being managed by anyone. Whom shall I put in charge?", "center_captured_lord_advice",
   []],
]
