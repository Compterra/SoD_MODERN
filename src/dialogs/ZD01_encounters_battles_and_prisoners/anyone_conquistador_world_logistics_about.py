DIALOGS = [
[anyone, "conquistador_world_logistics_about", [
   (call_script, "script_sod_conquistador_describe_status_to_s25"),
   (assign, ":employer_faction", 0),
   (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
     (eq, ":employer_faction", 0),
     (faction_slot_eq, ":cur_faction", slot_faction_merc_pact, "fac_sod_merc_guild2"),
     (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
     (assign, ":employer_faction", ":cur_faction"),
   (try_end),
   (try_begin),
     (gt, ":employer_faction", 0),
     (str_store_faction_name, s4, ":employer_faction"),
   (else_try),
     (str_store_string, s4, "@our own quartermasters"),
   (try_end),
  ], "{s4} pays for the campaign. We decide what it needs: iron for plates, horseflesh for lancers, bolts for crossbows, and coin enough to keep discipline from rusting. {s25}", "conquistador_world_logistics_talk", []],
]
