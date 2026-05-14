DIALOGS = [
[party_tpl|pt_jotnar_hearth_guard, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild4", "fac_player_supporters_faction"),
   (lt, ":relation", 0),
  ], "Hands open. We are Jotnar hearth guard. If you came hunting weak fires, you found the people who stand in front of them.", "jotnar_world_hearth_talk", []],
[party_tpl|pt_jotnar_hearth_guard, "start", [
   (eq, "$talk_context", tc_party_encounter),
   (store_relation, ":relation", "fac_sod_merc_guild4", "fac_player_supporters_faction"),
   (ge, ":relation", 20),
  ], "Come in slowly, friend of the hearth. We guard clan fires and villages that still have life enough to save.", "jotnar_world_hearth_talk", []],
[party_tpl|pt_jotnar_hearth_guard, "start", [
   (eq, "$talk_context", tc_party_encounter),
  ], "Keep your hands where we can see them. We are Jotnar hearth guard, walking between clan fires and villages that still have life enough to save.", "jotnar_world_hearth_talk", []],
]
