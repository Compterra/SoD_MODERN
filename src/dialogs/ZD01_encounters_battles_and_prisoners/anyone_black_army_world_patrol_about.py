DIALOGS = [
[anyone, "black_army_world_patrol_about", [
   (call_script, "script_sod_black_army_describe_status_to_s24"),
   (assign, ":employer_faction", 0),
   (try_for_range, ":cur_faction", native_kingdoms_begin, native_kingdoms_end),
     (eq, ":employer_faction", 0),
     (faction_slot_eq, ":cur_faction", slot_faction_merc_pact, "fac_sod_merc_guild1"),
     (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
     (assign, ":employer_faction", ":cur_faction"),
   (try_end),
   (try_begin),
     (gt, ":employer_faction", 0),
     (str_store_faction_name, s4, ":employer_faction"),
   (else_try),
     (str_store_string, s4, "@the Black Army"),
   (try_end),
  ], "The coin names {s4}; the work names itself. Bandits, deserters, and broken roads cost everyone more than our fee. {s24}", "black_army_world_patrol_talk", []],
]
