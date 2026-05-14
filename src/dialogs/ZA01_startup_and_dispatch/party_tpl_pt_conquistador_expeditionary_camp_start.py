DIALOGS = [
[party_tpl|pt_conquistador_expeditionary_camp, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild2", "fac_player_supporters_faction"),
   (lt, ":relation", 0),
  ], "You approach a Conquistador expeditionary camp under hard watch. We do not hold land, but we do remember who threatens the supply lines that keep men alive.", "conquistador_world_logistics_talk", []],
[party_tpl|pt_conquistador_expeditionary_camp, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild2", "fac_player_supporters_faction"),
   (ge, ":relation", 20),
  ], "You approach a Conquistador expeditionary camp. If you have brought news, supplies, or clean terms, the quartermasters will hear you before the captains do.", "conquistador_world_logistics_talk", []],
[party_tpl|pt_conquistador_expeditionary_camp, "start", [
   (eq, "$talk_context", tc_party_encounter),
  ], "You approach an expeditionary camp of the Conquistadors. We are not here to hold land. We keep an army moving where lesser companies would starve.", "conquistador_world_logistics_talk", []],
]
