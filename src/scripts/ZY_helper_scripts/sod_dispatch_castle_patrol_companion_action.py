# COST: low
SCRIPTS = [
("sod_dispatch_castle_patrol_companion_action",
 [
   (store_script_param, ":role", 1),
   (store_script_param, ":weight", 2),
   (try_begin),
     (eq, ":role", sod_castle_patrol_role_village_shield),
     (call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_castle_patrol_village_shield, ":weight"),
   (else_try),
     (eq, ":role", sod_castle_patrol_role_road),
     (call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_castle_patrol_road_control, ":weight"),
   (else_try),
     (eq, ":role", sod_castle_patrol_role_border_harasser),
     (call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_castle_patrol_border_harass, ":weight"),
   (else_try),
     (eq, ":role", sod_castle_patrol_role_caravan_screen),
     (call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_castle_patrol_caravan_screen, ":weight"),
   (else_try),
     (eq, ":role", sod_castle_patrol_role_emergency_relief),
     (call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_castle_patrol_village_shield, ":weight"),
   (try_end),
 ]),
]
