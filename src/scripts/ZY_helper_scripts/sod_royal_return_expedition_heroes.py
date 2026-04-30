# COST: low
SCRIPTS = [
("sod_royal_return_expedition_heroes",
 [
   (store_script_param_1, ":return_mode"),

   (assign, ":heroes", "$sod_royal_heroes"),
   (try_begin),
     (eq, ":return_mode", 0),
     (gt, "$sod_royal_heroes", 0),
     (store_add, ":heroes_plus_1", "$sod_royal_heroes", 1),
     (store_random_in_range, ":heroes", 1, ":heroes_plus_1"),
   (try_end),

   (assign, ":done", 0),
   (assign, ":center", "p_main_party"),
   (str_clear, s21),
   (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
     (eq, ":done", 0),
     (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
     (assign, ":center", ":center_no"),
     (str_store_party_name, s21, ":center"),
     (str_store_string, s21, "@They are currently resting at {s21}."),
     (assign, ":done", 1),
   (try_end),

   (try_begin),
     (gt, ":heroes", 0),
     (party_add_members, ":center", "$sod_royal_hero", ":heroes"),
   (try_end),

   (assign, reg21, ":heroes"),
   (assign, reg22, "$sod_royal_heroes"),
   (try_begin),
     (eq, reg21, reg22),
     (str_store_string, s22, "@All"),
   (else_try),
     (str_store_string, s22, "@{reg21} of {reg22}"),
   (try_end),
 ]),
]
