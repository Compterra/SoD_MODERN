DIALOGS = [
[anyone|plyr, "party_encounter_mercs", [
  ],"Surrender or die!", "party_encounter_mercs_attack", [
  (party_get_slot, ":troop", "$g_encountered_party", slot_party_boss),
  (store_troop_faction, ":troop_fac", ":troop"),
  (call_script, "script_make_kingdom_hostile_to_player", ":troop_fac", -3),
  (assign, "$g_enemy_party", "$g_encountered_party"),
  (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
  ]],
]
