SCRIPTS = [
("sod_center_process_daily_castle_food_resupply",
 [
       (try_for_range, ":center_no", castles_begin, castles_end),
         (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), # castle is not under siege
         (party_get_slot, ":center_food_store", ":center_no", slot_party_food_store),
         (call_script, "script_center_get_food_store_limit", ":center_no"),
         (assign, ":food_store_limit", reg0),
         (call_script, "script_center_get_food_consumption", ":center_no"),
         (assign, ":food_consumption", reg0),
         (party_get_slot, ":center_wealth", ":center_no", slot_town_wealth),
         (val_max, ":center_wealth", 0),
         (call_script, "script_sod_get_castle_support_profile", ":center_no"),
         (assign, ":castle_support", reg0),
         (assign, ":garrison", reg1),
         (assign, ":support_population", reg2),
         (assign, ":food_security", reg4),
         (assign, ":road_control", reg6),

         # Daily replenishment should reflect actual demand rather than a flat +240.
         # Small garrisons recover slowly; large garrisons need stronger peacetime resupply.
         (assign, ":daily_restock", 120),
         (val_add, ":daily_restock", ":food_consumption"),
         (val_div, ":daily_restock", 2),
         (store_div, ":support_bonus", ":support_population", 80),
         (val_add, ":daily_restock", ":support_bonus"),
         (store_div, ":castle_support_bonus", ":castle_support", 4),
         (val_add, ":daily_restock", ":castle_support_bonus"),

         # If stores are badly depleted, push extra catch-up supply into the center.
         (store_div, ":quarter_limit", ":food_store_limit", 4),
         (store_div, ":half_limit", ":food_store_limit", 2),
         (try_begin),
           (lt, ":center_food_store", ":quarter_limit"),
           (store_div, ":emergency_boost", ":food_consumption", 2),
           (val_add, ":daily_restock", ":emergency_boost"),
           (val_add, ":daily_restock", 60),
         (else_try),
           (lt, ":center_food_store", ":half_limit"),
           (store_div, ":recovery_boost", ":food_consumption", 4),
           (val_add, ":daily_restock", ":recovery_boost"),
           (val_add, ":daily_restock", 30),
         (try_end),

         # Near-full stores should taper off instead of endlessly refilling at full pace.
         (store_mul, ":three_quarter_limit", ":food_store_limit", 3),
         (val_div, ":three_quarter_limit", 4),
         (try_begin),
           (gt, ":center_food_store", ":three_quarter_limit"),
           (store_div, ":overflow_slowdown", ":daily_restock", 3),
           (val_sub, ":daily_restock", ":overflow_slowdown"),
         (try_end),

         # Castles without money or bound-village labor can still forage, but recover slowly.
         (assign, ":resupply_capacity", 30),
         (store_div, ":wealth_capacity", ":center_wealth", 12),
         (val_add, ":resupply_capacity", ":wealth_capacity"),
         (store_div, ":population_capacity", ":support_population", 35),
         (val_add, ":resupply_capacity", ":population_capacity"),
         (store_div, ":garrison_capacity", ":garrison", 8),
         (val_add, ":resupply_capacity", ":garrison_capacity"),
         (store_div, ":road_capacity", ":road_control", 2),
         (val_add, ":resupply_capacity", ":road_capacity"),
         (store_div, ":food_network_capacity", ":food_security", 40),
         (val_add, ":resupply_capacity", ":food_network_capacity"),
         (val_clamp, ":resupply_capacity", 30, 561),
         (val_min, ":daily_restock", ":resupply_capacity"),

         # Safety: keep daily resupply bounded and non-negative.
         (val_clamp, ":daily_restock", 20, 561),

         (store_div, ":resupply_cost", ":daily_restock", 3),
         (val_min, ":resupply_cost", ":center_wealth"),
         (store_sub, ":wealth_cost", 0, ":resupply_cost"),
         (call_script, "script_sod_change_center_wealth", ":center_no", ":wealth_cost"),

         (call_script, "script_sod_center_apply_food_delta", ":center_no", ":daily_restock"),
       (try_end),
 ]),
]
