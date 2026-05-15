DIALOGS = [
[anyone|plyr, "village_elder_talk",
  [
    (is_between, "$current_town", villages_begin, villages_end),
    (call_script, "script_sod_center_public_health_compute_causes", "$current_town"),
    (assign, ":risk", reg4),
    (party_get_slot, ":health", "$current_town", slot_center_sod_local_health),
    (party_get_slot, ":outbreak", "$current_town", slot_center_health_outbreak_type),
    (party_get_slot, ":aftermath", "$current_town", slot_center_health_recent_aftermath),
    (this_or_next|gt, ":outbreak", sod_outbreak_none),
    (this_or_next|gt, ":aftermath", 0),
    (this_or_next|ge, ":risk", 50),
    (lt, ":health", 40),
  ],
   "What does the village need to keep sickness away?", "village_elder_public_health", []],
]
