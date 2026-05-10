SIMPLE_TRIGGERS = [
  (24,
   [
     # Campaign modernization cadence: daily world-presence, diplomacy,
     # companion, and lord morale pulse. Keep this trigger declarative.
     (call_script, "script_sod_jotnar_process_world_activity"),
     (call_script, "script_sod_elephant_guard_process_world_activity"),
     (call_script, "script_sod_black_khergits_spawn_raids"),
     (call_script, "script_sod_imperial_expedition_process_campaign"),
     (call_script, "script_sod_diplomacy_process_envoy_parties"),
     (call_script, "script_sod_diplomacy_process_decrees"),
     (call_script, "script_sod_diplomacy_update_realm_state"),
     (call_script, "script_sod_mini_faction_process_threshold_incidents"),
     (call_script, "script_sod_companion_process_daily_depth"),
     (call_script, "script_sod_lord_update_all_party_morale"),
     (try_begin),
       (neq, "$g_sod_lord_offers_allegience", 0),
       (start_map_conversation, "$g_sod_lord_offers_allegience"),
     (try_end),
   ]),
]
