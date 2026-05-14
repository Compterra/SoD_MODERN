DIALOGS = [
[party_tpl|pt_elephant_guard_sanctuary_patrol, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild3", "fac_player_supporters_faction"),
   (lt, ":relation", 0),
  ], "Walk carefully. The Elephant's shadow is shelter to the frightened and weight upon the cruel. If you bring more blood to this road, we will answer it.", "elephant_guard_world_talk", []],
[party_tpl|pt_elephant_guard_sanctuary_patrol, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild3", "fac_player_supporters_faction"),
   (ge, ":relation", 20),
  ], "Peace to your road. The villages know your name without spitting after it, so speak plainly under Elephant's shadow.", "elephant_guard_world_talk", []],
[party_tpl|pt_elephant_guard_sanctuary_patrol, "start", [
   (eq, "$talk_context", tc_party_encounter),
  ], "Walk carefully, traveler. This road lies beneath Elephant's shadow, and the villages near it have already endured enough blood.", "elephant_guard_world_talk", []],
]
