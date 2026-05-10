DIALOGS = [
[anyone|plyr, "village_elder_talk",
   [
     (party_get_slot, ":pressure", "$current_town", slot_center_sod_looter_raid_pressure),
     (party_get_slot, ":last_raid_day", "$current_town", slot_center_sod_looter_last_raid_day),
     (party_get_slot, ":last_defense_day", "$current_town", slot_center_sod_looter_last_defense_day),
     (party_get_slot, ":last_assault_day", "$current_town", slot_center_sod_looter_last_assault_day),
     (store_current_day, ":current_day"),
     (store_mul, ":recent_window", sod_looter_raid_village_cooldown_days, 2),
     (store_sub, ":raid_age", ":current_day", ":last_raid_day"),
     (store_sub, ":defense_age", ":current_day", ":last_defense_day"),
     (store_sub, ":assault_age", ":current_day", ":last_assault_day"),
     (this_or_next|gt, ":pressure", 0),
     (this_or_next|is_between, ":raid_age", 0, ":recent_window"),
     (this_or_next|is_between, ":defense_age", 0, ":recent_window"),
     (is_between, ":assault_age", 0, ":recent_window"),
   ],
   "How bad is the looter trouble on your roads?", "village_elder_looter_pressure", []],
]
