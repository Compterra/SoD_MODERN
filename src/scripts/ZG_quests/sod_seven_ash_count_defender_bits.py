SCRIPTS = [
("sod_seven_ash_count_defender_bits",
    [
      (store_script_param, ":bitmask", 1),
      (assign, ":count", 0),
      (try_begin), (store_and, ":bit", ":bitmask", sod_seven_ash_defender_garric), (gt, ":bit", 0), (val_add, ":count", 1), (try_end),
      (try_begin), (store_and, ":bit", ":bitmask", sod_seven_ash_defender_oswin), (gt, ":bit", 0), (val_add, ":count", 1), (try_end),
      (try_begin), (store_and, ":bit", ":bitmask", sod_seven_ash_defender_aldrik), (gt, ":bit", 0), (val_add, ":count", 1), (try_end),
      (try_begin), (store_and, ":bit", ":bitmask", sod_seven_ash_defender_mirelle), (gt, ":bit", 0), (val_add, ":count", 1), (try_end),
      (try_begin), (store_and, ":bit", ":bitmask", sod_seven_ash_defender_tomas), (gt, ":bit", 0), (val_add, ":count", 1), (try_end),
      (try_begin), (store_and, ":bit", ":bitmask", sod_seven_ash_defender_beren), (gt, ":bit", 0), (val_add, ":count", 1), (try_end),
      (try_begin), (store_and, ":bit", ":bitmask", sod_seven_ash_defender_elianor), (gt, ":bit", 0), (val_add, ":count", 1), (try_end),
      (assign, reg0, ":count"),
  ]),
]
