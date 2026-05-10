# COST: low
SCRIPTS = [
("sod_trim_party_active_troops",
 [
   (store_script_param, ":party_no", 1),
   (store_script_param, ":max_active", 2),
   (party_get_num_companions, ":active_size", ":party_no"),
   (try_for_range, ":unused", 0, 50),
     (gt, ":active_size", ":max_active"),
     (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
     (gt, ":num_stacks", 0),
     (store_sub, ":last_stack", ":num_stacks", 1),
     (party_stack_get_troop_id, ":troop_id", ":party_no", ":last_stack"),
     (neg|troop_is_hero, ":troop_id"),
     (party_stack_get_size, ":stack_size", ":party_no", ":last_stack"),
     (store_sub, ":excess", ":active_size", ":max_active"),
     (val_min, ":excess", ":stack_size"),
     (party_remove_members, ":party_no", ":troop_id", ":excess"),
     (val_sub, ":active_size", ":excess"),
   (try_end),
   (assign, reg0, ":active_size"),
 ]),
]
