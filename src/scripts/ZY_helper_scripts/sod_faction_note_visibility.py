# COST: medium; scans centers and kingdom heroes only while a faction note is refreshed.
# Placeholder realms should not enter the Notes faction list until they have a real foothold.
SCRIPTS = [
("sod_faction_should_show_notes",
 [
   (store_script_param_1, ":faction_no"),
   (assign, reg0, 1),

   # Defeated native kingdoms intentionally retain their historical Notes entry.
   # Only the seven dormant realm slots below need a real foothold before they
   # become discoverable through the faction list.
   (assign, ":requires_realm_presence", 0),
   (try_begin),
     (this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
     (this_or_next|eq, ":faction_no", "fac_kingdom_6"),
     (is_between, ":faction_no", rebel_factions_begin, rebel_factions_end),
     (assign, ":requires_realm_presence", 1),
   (try_end),

   (try_begin),
     (eq, ":requires_realm_presence", 1),
     (assign, reg0, 0),
     (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),

     (assign, ":has_fief", 0),
     (try_for_range, ":center_no", centers_begin, centers_end),
       (store_faction_of_party, ":center_faction", ":center_no"),
       (eq, ":center_faction", ":faction_no"),
       (assign, ":has_fief", 1),
     (try_end),

     (assign, ":has_vassal", 0),
     (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
     (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
       (store_troop_faction, ":troop_faction", ":troop_no"),
       (eq, ":troop_faction", ":faction_no"),
       (neq, ":troop_no", ":faction_leader"),
       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
       (assign, ":has_vassal", 1),
     (try_end),

     (try_begin),
       (this_or_next|eq, ":has_fief", 1),
       (eq, ":has_vassal", 1),
       (assign, reg0, 1),
     (try_end),
   (try_end),
 ]),
]
