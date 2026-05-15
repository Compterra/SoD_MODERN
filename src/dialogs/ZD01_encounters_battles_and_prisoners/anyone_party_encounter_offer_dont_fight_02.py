DIALOGS = [
[anyone, "party_encounter_offer_dont_fight", [], "Ha-ha. But I want to fight with you.", "close_window", [
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  (encounter_attack),
]],
]
