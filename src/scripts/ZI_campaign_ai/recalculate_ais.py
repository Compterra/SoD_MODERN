SCRIPTS = [
("recalculate_ais",
    [
      (call_script, "script_init_ai_calculation"),

      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neg|faction_slot_eq, ":faction_no",  slot_faction_marshall, "trp_player"),
        (call_script, "script_decide_faction_ai", ":faction_no"),
      (try_end),
      (call_script, "script_decide_kingdom_party_ais"),
  ]),
]
