SCRIPTS = [
("copy_upgrade_to_all_heroes",
                      [
                        (store_script_param_1, ":troop"),

                        (troop_get_slot, ":upg_armor", ":troop", slot_troop_upgrade_armor),
                        (troop_get_slot, ":upg_horse", ":troop", slot_troop_upgrade_horse),
                        (troop_get_slot, ":upg_wpn0", ":troop", slot_troop_upgrade_wpn_0),
                        (troop_get_slot, ":upg_wpn1", ":troop", slot_troop_upgrade_wpn_1),
                        (troop_get_slot, ":upg_wpn2", ":troop", slot_troop_upgrade_wpn_2),
                        (troop_get_slot, ":upg_wpn3", ":troop", slot_troop_upgrade_wpn_3),

                        (try_for_range, ":hero", companions_begin, companions_end),
                          (troop_set_slot, ":hero", slot_troop_upgrade_armor, ":upg_armor"),
                          (troop_set_slot, ":hero", slot_troop_upgrade_horse, ":upg_horse"),
                          (troop_set_slot, ":hero", slot_troop_upgrade_wpn_0, ":upg_wpn0"),
                          (troop_set_slot, ":hero", slot_troop_upgrade_wpn_1, ":upg_wpn1"),
                          (troop_set_slot, ":hero", slot_troop_upgrade_wpn_2, ":upg_wpn2"),
                          (troop_set_slot, ":hero", slot_troop_upgrade_wpn_3, ":upg_wpn3"),
                        (try_end),
                      ]
                    ),
]
