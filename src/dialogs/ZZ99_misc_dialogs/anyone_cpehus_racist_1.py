DIALOGS = [
[anyone, "cpehus_racist_1", [], "You truly think your gathering of village idiots can overcome the Imperial Legion ? The destruction I brought to your homeland will seem gentle in comparison to what I'm going to do to your precious kingdom after I'm through with you, simpleton.", "close_window", [
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  (encounter_attack)] ],
]
