SIMPLE_TRIGGERS = [
  (24,
   [
     # Keep kingdom trade visible on the world map. The caravan behavior and
     # trade engine already exist; this daily pulse supplies new caravans up to
     # each faction's configured cap.
     (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
       (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
       (faction_get_slot, ":num_towns", ":faction_no", slot_faction_num_towns),
       (gt, ":num_towns", 0),
       (call_script, "script_create_kingdom_party_if_below_limit", ":faction_no", spt_kingdom_caravan),
     (try_end),
   ]),
]
