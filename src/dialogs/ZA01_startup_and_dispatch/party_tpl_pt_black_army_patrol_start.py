DIALOGS = [
[party_tpl|pt_black_army_patrol, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild1", "fac_player_supporters_faction"),
   (lt, ":relation", 0),
  ], "Hold and keep your hands honest. Black Army road detail. Our contract says this stretch stays open; it does not say we must be gentle with people who make it expensive.", "black_army_world_patrol_talk", []],
[party_tpl|pt_black_army_patrol, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild1", "fac_player_supporters_faction"),
   (ge, ":relation", 20),
  ], "Easy on the reins. You are known well enough that nobody here needs to prove courage. Black Army road detail; we are keeping the stretch passable and the account clean.", "black_army_world_patrol_talk", []],
[party_tpl|pt_black_army_patrol, "start", [
   (eq, "$talk_context", tc_party_encounter),
  ], "Hold. Black Army road detail. We are paid to keep this stretch passable, count threats before pride, and make trouble choose a cheaper road.", "black_army_world_patrol_talk", []],
]
