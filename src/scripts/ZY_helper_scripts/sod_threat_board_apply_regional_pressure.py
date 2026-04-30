# COST: low
SCRIPTS = [
("sod_threat_board_apply_regional_pressure",
 [
   (store_script_param_1, ":threat_type"),
   (store_script_param_2, ":sponsor_center"),

   (try_begin),
     (eq, ":threat_type", sod_threat_type_cattle_raiders),
     (party_get_slot, ":cattle", ":sponsor_center", slot_village_number_of_cattle),
     (val_sub, ":cattle", 8),
     (val_max, ":cattle", 0),
     (party_set_slot, ":sponsor_center", slot_village_number_of_cattle, ":cattle"),
     (call_script, "script_change_player_relation_with_center", ":sponsor_center", -2),
   (else_try),
     (eq, ":threat_type", sod_threat_type_rogue_company),
     (call_script, "script_change_player_relation_with_center", ":sponsor_center", -1),
   (else_try),
     (eq, ":threat_type", sod_threat_type_relic_thieves),
     (call_script, "script_change_player_relation_with_center", ":sponsor_center", -1),
   (else_try),
     (call_script, "script_change_player_relation_with_center", ":sponsor_center", -1),
   (try_end),
 ]),
]
