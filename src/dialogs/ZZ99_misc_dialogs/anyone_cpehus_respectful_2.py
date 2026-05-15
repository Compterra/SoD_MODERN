DIALOGS = [
[anyone, "cpehus_respectful_2", [], "When the battle is over and the sternly raging dust of the land settles, revealing the corpses of your loyal companions, you will feel the true burden of your royal authority.", "close_window", [
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  (encounter_attack)] ],
]
