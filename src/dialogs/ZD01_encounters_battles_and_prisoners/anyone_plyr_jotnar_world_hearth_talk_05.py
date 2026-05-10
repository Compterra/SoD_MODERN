DIALOGS = [
[anyone|plyr, "jotnar_world_hearth_talk", [
   (store_relation, ":relation", "fac_player_supporters_faction", "fac_sod_merc_guild4"),
   (ge, ":relation", 5),
   (faction_get_slot, ":hearth_pressure", "fac_sod_merc_guild4", slot_faction_jotnar_hearth_pressure),
   (lt, ":hearth_pressure", 70),
   (party_count_members_of_type, ":male_slaves", "p_main_party", "trp_slave"),
   (party_count_members_of_type, ":female_slaves", "p_main_party", "trp_slave_female"),
   (store_add, ":slave_count", ":male_slaves", ":female_slaves"),
   (eq, ":slave_count", 0),
   (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
   (gt, ":free_capacity", 0),
   (store_current_day, ":cur_day"),
   (store_sub, ":days_since_volunteers", ":cur_day", "$g_sod_jotnar_last_volunteer_day"),
   (this_or_next|ge, ":days_since_volunteers", 14),
   (lt, "$g_sod_jotnar_last_volunteer_day", 1),
  ], "Can any hearth fighters join my company?", "jotnar_world_hearth_volunteers", [
    (call_script, "script_sod_jotnar_grant_hearth_volunteers"),
  ]],
]
