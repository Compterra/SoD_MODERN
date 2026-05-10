DIALOGS = [
[anyone|plyr, "elephant_guard_world_talk", [
   (ge, "$player_honor", 5),
   (store_relation, ":relation", "fac_player_supporters_faction", "fac_sod_merc_guild3"),
   (ge, ":relation", 5),
   (party_count_members_of_type, ":male_slaves", "p_main_party", "trp_slave"),
   (party_count_members_of_type, ":female_slaves", "p_main_party", "trp_slave_female"),
   (store_add, ":slave_count", ":male_slaves", ":female_slaves"),
   (eq, ":slave_count", 0),
   (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
   (gt, ":free_capacity", 0),
   (store_current_day, ":cur_day"),
   (store_sub, ":days_since_volunteers", ":cur_day", "$g_sod_elephant_guard_last_volunteer_day"),
   (this_or_next|ge, ":days_since_volunteers", 14),
   (lt, "$g_sod_elephant_guard_last_volunteer_day", 1),
  ], "Can any shrine-road warriors join my company?", "elephant_guard_world_volunteers", [
    (call_script, "script_sod_elephant_guard_grant_road_volunteers"),
  ]],
]
