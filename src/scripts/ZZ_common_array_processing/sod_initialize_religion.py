SCRIPTS = [
("sod_initialize_religion",
  [
    (call_script, "script_sod_troop_init_doctrine_registry"),

    (call_script, "script_sod_troop_get_faith_upgrade", "trp_sod_ant_honor_guard1"),
    (troop_set_slot, "trp_sod_ant_honor_guard1", slot_troop_sod_upgrade1, reg0),
    (troop_set_slot, "trp_sod_ant_honor_guard1", slot_troop_sod_doctrine_faith_upgrade, reg0),

    (call_script, "script_sod_troop_get_faith_upgrade", "trp_sod_mar_condottieri1"),
    (troop_set_slot, "trp_sod_mar_condottieri1", slot_troop_sod_upgrade1, reg0),
    (troop_set_slot, "trp_sod_mar_condottieri1", slot_troop_sod_doctrine_faith_upgrade, reg0),

    (call_script, "script_sod_troop_get_faith_upgrade", "trp_sod_vil_high_chief1"),
    (troop_set_slot, "trp_sod_vil_high_chief1", slot_troop_sod_upgrade1, reg0),
    (troop_set_slot, "trp_sod_vil_high_chief1", slot_troop_sod_doctrine_faith_upgrade, reg0),

    (call_script, "script_sod_troop_get_faith_upgrade", "trp_sod_ade_magnate1"),
    (troop_set_slot, "trp_sod_ade_magnate1", slot_troop_sod_upgrade1, reg0),
    (troop_set_slot, "trp_sod_ade_magnate1", slot_troop_sod_doctrine_faith_upgrade, reg0),

    (call_script, "script_sod_troop_get_faith_upgrade", "trp_sod_zer_3_noble1"),
    (troop_set_slot, "trp_sod_zer_3_noble1", slot_troop_sod_upgrade1, reg0),
    (troop_set_slot, "trp_sod_zer_3_noble1", slot_troop_sod_doctrine_faith_upgrade, reg0),
  ]),
]
