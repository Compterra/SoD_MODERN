SIMPLE_TRIGGERS = [
(24,
   [
     (try_for_range, ":rebel_faction", rebel_factions_begin, rebel_factions_end),
       (faction_slot_eq, ":rebel_faction", slot_faction_state, sfs_active),
       (faction_slot_eq, ":rebel_faction", slot_faction_sod_civil_war_state, sod_civil_war_open_rebellion),
       (call_script, "script_sod_claimant_maintain_rebel_ai", ":rebel_faction"),
       (call_script, "script_sod_claimant_civil_war_check_resolution", ":rebel_faction"),
     (try_end),
   ]),
]
