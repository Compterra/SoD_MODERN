DIALOGS = [
[anyone, "gm_pretalk", [
   (call_script, "script_sod_store_guild_master_social_weather_to_s12", "$g_talk_troop"),
   (eq, reg0, 1),
  ], "{s12}", "gm_talk", [
   (faction_get_slot, ":mercs", "fac_player_faction", slot_faction_merc_pact),
   (faction_set_slot, "fac_player_supporters_faction", slot_faction_merc_pact, ":mercs"),
   (call_script, "script_update_faction_notes", "fac_player_supporters_faction"),
   (call_script, "script_update_faction_notes", ":mercs"),
   (faction_get_slot, ":base", ":mercs", slot_guild_base),
   (party_get_slot, ":leader", ":base", slot_town_lord),
   (call_script, "script_update_troop_notes", ":leader"),
   (store_relation, "$g_talk_troop_faction_relation", "$g_talk_troop_faction", "fac_player_faction"),
  ]],
]
