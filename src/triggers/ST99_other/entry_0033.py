SIMPLE_TRIGGERS = [
(36,
   [
     (try_for_range, ":troop_no", heroes_begin, heroes_end),
       (troop_set_slot, ":troop_no", slot_troop_does_not_give_quest, 0),
     (try_end),

     (try_for_range, ":troop_no", village_elders_begin, village_elders_end),
       (troop_set_slot, ":troop_no", slot_troop_does_not_give_quest, 0),
     (try_end),
    ]),
]
