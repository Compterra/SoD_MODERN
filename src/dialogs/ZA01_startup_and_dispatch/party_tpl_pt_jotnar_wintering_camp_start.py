DIALOGS = [
[party_tpl|pt_jotnar_wintering_camp, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild4", "fac_player_supporters_faction"),
   (lt, ":relation", 0),
  ], "This is a Jotnar wintering camp. Families sleep behind those shields. Take one step like a raider and every cooking fire becomes a war fire.", "jotnar_world_hearth_talk", []],
[party_tpl|pt_jotnar_wintering_camp, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild4", "fac_player_supporters_faction"),
   (ge, ":relation", 20),
  ], "This is a Jotnar wintering camp. If your road is cold, stand near the outer fire and speak. Guests are measured by what they protect.", "jotnar_world_hearth_talk", []],
[party_tpl|pt_jotnar_wintering_camp, "start", [
   (eq, "$talk_context", tc_party_encounter),
  ], "This is a Jotnar wintering camp, not a lord's army. Our families, stores, and shield bands settle where fields need hands and roads need teeth.", "jotnar_world_hearth_talk", []],
]
