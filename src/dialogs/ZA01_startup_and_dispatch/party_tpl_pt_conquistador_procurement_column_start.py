DIALOGS = [
[party_tpl|pt_conquistador_procurement_column, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild2", "fac_player_supporters_faction"),
   (lt, ":relation", 0),
  ], "Stand aside and do not touch the packs. This is a Conquistador procurement column, and hostile hands near army stores are counted as thieves before they are counted as soldiers.", "conquistador_world_logistics_talk", []],
[party_tpl|pt_conquistador_procurement_column, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild2", "fac_player_supporters_faction"),
   (ge, ":relation", 20),
  ], "Good, a known face. Keep pace if you want to talk; iron, horses, grain, and cordage do not become an army by standing in the road.", "conquistador_world_logistics_talk", []],
[party_tpl|pt_conquistador_procurement_column, "start", [
   (eq, "$talk_context", tc_party_encounter),
  ], "Stand aside, traveler. This is a Conquistador procurement column. Iron, horses, grain, cordage: without them, even the finest army dies in place.", "conquistador_world_logistics_talk", []],
]
