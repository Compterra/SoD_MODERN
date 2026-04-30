# COST: low
SCRIPTS = [
("merc_sync_player_guild_pact",
 [
   (store_script_param_1, ":guild_no"),

   (faction_set_slot, "fac_player_faction", slot_faction_merc_pact, ":guild_no"),
   (faction_set_slot, "fac_player_supporters_faction", slot_faction_merc_pact, ":guild_no"),

   (call_script, "script_update_faction_notes", "fac_player_supporters_faction"),
   (try_begin),
     (gt, ":guild_no", 0),
     (call_script, "script_update_faction_notes", ":guild_no"),
     (faction_get_slot, ":base", ":guild_no", slot_guild_base),
     (gt, ":base", 0),
     (party_get_slot, ":leader", ":base", slot_town_lord),
     (gt, ":leader", 0),
     (call_script, "script_update_troop_notes", ":leader"),
   (try_end),
 ]),
]
