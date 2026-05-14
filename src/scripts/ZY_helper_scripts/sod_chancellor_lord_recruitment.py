# COST: low
SCRIPTS = [
("sod_chancellor_lord_recruitment_refresh",
 [
   # Include the player: the kingdom needs one income-producing center for
   # each lord, plus one more to support the crown.
   (assign, ":num_lords", 1),
   (try_for_range, ":lord", kingdom_heroes_begin, kingdom_heroes_end),
     (troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
     (store_troop_faction, ":faction", ":lord"),
     (this_or_next|eq, ":faction", "fac_player_supporters_faction"),
     (is_between, ":lord", "trp_reserved_knight_1", "trp_knight_6_01"),
     (val_add, ":num_lords", 1),
   (try_end),

   (assign, ":num_centers", 0),
   (try_for_range, ":center_no", centers_begin, centers_end),
     (store_faction_of_party, ":center_faction", ":center_no"),
     (eq, ":center_faction", "fac_player_supporters_faction"),
     (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
     (val_add, ":num_centers", 1),
   (try_end),

   (store_sub, "$territory", ":num_centers", ":num_lords"),

   (assign, "$lords", 0),
   (try_for_range, ":lord", "trp_reserved_knight_1", "trp_knight_6_01"),
     (neg|troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
     (neg|troop_slot_eq, ":lord", slot_troop_occupation, slto_dead),
     (troop_set_slot, "trp_temp_array_a", "$lords", ":lord"),
     (val_add, "$lords", 1),
   (try_end),

   (try_begin),
     (lt, "$lords", 1),
     (str_store_string, s60, "@There are no homeland lords left who can answer a summons to court."),
   (else_try),
     (ge, "$territory", 1),
     (assign, reg1, "$territory"),
     (try_begin),
       (gt, "$territory", 1),
       (str_store_string, s60, "@The rolls can support {reg1} more lords. A new oath would be credible, provided we grant land quickly."),
     (else_try),
       (str_store_string, s60, "@The rolls can support one more lord. A new oath would be credible, provided we grant land quickly."),
     (try_end),
   (else_try),
     (str_store_string, s60, "@The rolls are too thin for another lord. We need one more income-producing fief before a new oath will hold."),
   (try_end),
 ]),

("sod_chancellor_recruit_homeland_lord",
 [
   (assign, "$temp_lord", 0),
   (call_script, "script_sod_chancellor_lord_recruitment_refresh"),
   (try_begin),
     (ge, "$lords", 1),
     (ge, "$territory", 1),

     (store_random_in_range, ":roll", 0, "$lords"),
     (troop_get_slot, ":lord", "trp_temp_array_a", ":roll"),
     (assign, "$temp_lord", ":lord"),

     (troop_set_slot, ":lord", slot_troop_change_to_faction, "fac_player_supporters_faction"),
     (troop_set_slot, ":lord", slot_troop_occupation, slto_kingdom_hero),
     (troop_set_slot, ":lord", slot_troop_wealth, recruited_lord_starting_funds),
     (troop_set_slot, ":lord", slot_troop_original_faction, "fac_player_supporters_faction"),

     (store_random_in_range, ":relation", 0, 11),
     (troop_set_slot, ":lord", slot_troop_player_relation, ":relation"),

     (call_script, "script_store_troop_name_link", s61, ":lord"),
     (str_store_string, s60, "@{s61} will be summoned, invested with rank, and announced as a lord of the realm."),
   (else_try),
     (lt, "$lords", 1),
     (str_store_string, s60, "@I apologize, {m'Lord/m'Lady}, but there is no one left who can heed your call for another lord."),
   (else_try),
     (str_store_string, s60, "@I apologize, {m'Lord/m'Lady}, but we need more income-producing fiefs before another lord can be supported."),
   (try_end),
 ]),
]
