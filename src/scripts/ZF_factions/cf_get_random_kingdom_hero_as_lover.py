SCRIPTS = [
("cf_get_random_kingdom_hero_as_lover",
    [
      #      (store_script_param_1, ":cur_lady"),


      #      (troop_get_slot, ":cur_father", ":cur_lady", slot_troop_father),
      #      (troop_get_slot, ":fathers_rank", ":cur_father", slot_troop_kingdom_rank),
      (assign, ":result", -1),
      (assign, ":count_heroes", 0),
      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_slot_eq, ":troop_no", slot_troop_lover, 0),
        (troop_slot_eq, ":troop_no", slot_troop_spouse, 0),
        #        (troop_get_slot, ":cur_rank", ":troop_no", slot_troop_kingdom_rank),
        #        (lt, ":cur_rank", ":fathers_rank"), # Only heroes with lower ranks may be the lovers of the daughters
        (val_add, ":count_heroes", 1),
      (try_end),
      (store_random_in_range, ":random_hero", 0, ":count_heroes"),
      (assign, ":count_heroes", 0),
      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
        (eq, ":result", -1),
        (troop_slot_eq, ":troop_no", slot_troop_lover, 0),
        (troop_slot_eq, ":troop_no", slot_troop_spouse, 0),
        #        (troop_get_slot, ":cur_rank", ":troop_no", slot_troop_kingdom_rank),
        #        (lt, ":cur_rank", ":fathers_rank"), # Only heroes with lower ranks may be the lovers of the daughters
        (val_add, ":count_heroes", 1),
        (gt, ":count_heroes", ":random_hero"),
        (assign, ":result", ":troop_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),
]
