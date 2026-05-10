DIALOGS = [
[anyone|plyr, "black_khergit_khan_talk", [
    (store_relation, ":relation", "fac_player_supporters_faction", "fac_black_khergits"),
    (ge, ":relation", 20),
    (faction_get_slot, ":pressure", "fac_black_khergits", slot_faction_black_khergit_pressure),
    (le, ":pressure", 25),
    (call_script, "script_sod_black_khergits_prepare_hire_offer"),
  ], "Your riders know me now. Before you move camp, lend me a few lances.", "black_khergit_khan_hire_offer", []],
]
