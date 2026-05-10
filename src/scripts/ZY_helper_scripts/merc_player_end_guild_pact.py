# COST: low
SCRIPTS = [
("merc_player_end_guild_pact",
 [
   (store_script_param_1, ":guild_no"),
   (store_script_param_2, ":reset_relation"),

   (try_begin),
     (eq, ":reset_relation", 1),
     (set_relation, "fac_player_faction", ":guild_no", 0),
     (set_relation, "fac_player_supporters_faction", ":guild_no", 0),
   (try_end),

   (assign, "$g_mercenary_guild_weekly_payment", 0),
   (assign, "$g_sod_merc_weekly_paiment_not_paid_in_a_row", 0),
   (assign, "$g_sod_merc_weekly_paiment_paid_in_a_row", 0),
   (call_script, "script_merc_sync_player_guild_pact", 0),

   (try_begin),
     (gt, ":guild_no", 0),
     (store_current_day, ":cur_day"),
     (faction_set_slot, ":guild_no", slot_faction_pact_broken_day, ":cur_day"),
     (call_script, "script_merc_update_guild_marshal_faction", ":guild_no", "fac_commoners"),
     (call_script, "script_update_faction_notes", ":guild_no"),
   (try_end),

   (call_script, "script_update_all_notes"),
 ]),
]
