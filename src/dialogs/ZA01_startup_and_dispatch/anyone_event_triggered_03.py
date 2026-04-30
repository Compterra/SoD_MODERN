DIALOGS = [
[anyone, "event_triggered",
   [
     (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "$g_talk_troop"),
     (ge, "$g_center_taken_by_player_faction", 0),
     (str_store_party_name, s1, "$g_center_taken_by_player_faction"),
     ],
   "{s1} is not being managed by anyone. Whom shall I put in charge?", "center_captured_lord_advice",
   []],
]
