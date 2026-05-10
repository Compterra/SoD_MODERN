DIALOGS = [
[anyone, "elephant_guard_world_about", [
   (party_get_slot, ":destination", "$g_encountered_party", slot_party_sod_elephant_guard_destination),
   (str_store_string, s4, "@the wounded roads"),
   (try_begin),
     (gt, ":destination", 0),
     (str_store_party_name, s4, ":destination"),
   (try_end),
   (party_get_slot, ":activity_type", "$g_encountered_party", slot_party_sod_elephant_guard_activity_type),
   (try_begin),
     (eq, ":activity_type", sod_elephant_guard_activity_procession),
     (str_store_string, s5, "@The relics are being carried toward {s4}. Where fear gathers, people remember promises better than banners."),
   (else_try),
     (str_store_string, s5, "@We patrol near {s4}. Bandits, hungry soldiers, and careless lords all learn to avoid a guarded shrine-road."),
   (try_end),
  ], "{s5}", "elephant_guard_world_talk", []],
]
