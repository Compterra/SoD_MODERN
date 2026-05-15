# COST: medium
SCRIPTS = [
("merc_player_start_guild_pact",
 [
   (store_script_param_1, ":guild_no"),
   (store_script_param_2, ":weekly_payment"),

   (assign, "$g_mercenary_guild_weekly_payment", ":weekly_payment"),
   (assign, "$g_sod_merc_weekly_paiment_not_paid_in_a_row", 0),
   (assign, "$g_sod_merc_weekly_paiment_paid_in_a_row", 0),

   (try_begin),
     (gt, ":guild_no", 0),
     (faction_set_slot, ":guild_no", player_debt_to_faction, 0),
   (try_end),

   (call_script, "script_merc_sync_player_guild_pact", ":guild_no"),

   (try_for_range, ":cur_kingdom", native_kingdoms_begin, native_kingdoms_end),
     (store_relation, ":cur_relation", ":cur_kingdom", "fac_player_faction"),
     (set_relation, ":cur_kingdom", ":guild_no", ":cur_relation"),
   (try_end),

   (store_relation, ":rel", "fac_player_supporters_faction", ":guild_no"),
   (val_max, ":rel", 50),
   (set_relation, "fac_player_faction", ":guild_no", ":rel"),
   (set_relation, "fac_player_supporters_faction", ":guild_no", ":rel"),

   (try_for_range, ":cur_faction", native_kingdoms_begin, native_kingdoms_end),
     (faction_get_slot, ":mercenaries", ":cur_faction", slot_faction_merc_pact),
     (eq, ":mercenaries", ":guild_no"),
     (faction_set_slot, ":cur_faction", slot_faction_merc_pact, 0),
   (try_end),

   (call_script, "script_merc_update_guild_marshal_faction", ":guild_no", "fac_player_supporters_faction"),
   (call_script, "script_update_all_notes"),
 ]),
]
