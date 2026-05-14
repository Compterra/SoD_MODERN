DIALOGS = [
[party_tpl|pt_serpent_host_route_screen, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild5", "fac_player_supporters_faction"),
   (lt, ":relation", 0),
  ], "Reins loose, hands visible. Serpent Host route screen. We ride ahead of contracts, and hostile riders are the first delay we remove.", "serpent_host_world_route_talk", []],
[party_tpl|pt_serpent_host_route_screen, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild5", "fac_player_supporters_faction"),
   (ge, ":relation", 20),
  ], "Easy on the reins. Serpent Host route screen. Your name travels well enough that we can spend less time reaching for blades.", "serpent_host_world_route_talk", []],
[party_tpl|pt_serpent_host_route_screen, "start", [
   (eq, "$talk_context", tc_party_encounter),
  ], "Easy on the reins. Serpent Host route screen. We ride ahead of contracts, caravans, and messages that cannot afford slow roads.", "serpent_host_world_route_talk", []],
]
