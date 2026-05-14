DIALOGS = [
[party_tpl|pt_serpent_host_courier_lance, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild5", "fac_player_supporters_faction"),
   (lt, ":relation", 0),
  ], "You have found a Serpent courier lance. That is unfortunate for anyone blocking the road. We are paid to make distance disappear, and enemies are distance with a pulse.", "serpent_host_world_route_talk", []],
[party_tpl|pt_serpent_host_courier_lance, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild5", "fac_player_supporters_faction"),
   (ge, ":relation", 20),
  ], "You have found a Serpent courier lance. Your name travels ahead of you, which saves everyone the trouble of proving speed with steel.", "serpent_host_world_route_talk", []],
[party_tpl|pt_serpent_host_courier_lance, "start", [
   (eq, "$talk_context", tc_party_encounter),
  ], "You have found a Serpent courier lance. We are paid to make distance disappear and danger think twice.", "serpent_host_world_route_talk", []],
]
