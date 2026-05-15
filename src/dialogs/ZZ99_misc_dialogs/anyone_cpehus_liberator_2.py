DIALOGS = [
[anyone, "cpehus_liberator_2", [], "Today, we together shall triumph against the tides of tyranny ! Today, swords shall rend, arrows will pierce and horseshoes will crush all who stands against us ! We are the Imperial Legion, and this day is a day of glory !", "close_window", [
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  (encounter_attack)] ],
]
