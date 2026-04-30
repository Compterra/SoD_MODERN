DIALOGS = [
[anyone,"gm_hire_elite", [
  (call_script, "script_merc_get_elite_relation_requirement", "$g_talk_troop_faction"),
  (assign, reg21, reg0),
  ], "These soldiers are the cream of the crop of our army, and we hire them only to trusted partners.^^Required relation: {reg21}.", "gm_pretalk",[]],
]
