SIMPLE_TRIGGERS = [
(24,
   [
       (try_for_range, ":center_no", castles_begin, castles_end),
         (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), #castle is not under siege
         (party_get_slot, ":center_food_store", ":center_no", slot_party_food_store),
         (call_script, "script_center_get_food_store_limit", ":center_no"),
         (assign, ":food_store_limit", reg0),
         (call_script, "script_center_get_food_consumption", ":center_no"),
         (assign, ":food_consumption", reg0),

         # Daily replenishment should reflect actual demand rather than a flat +240.
         # Small garrisons recover slowly; large garrisons need stronger peacetime resupply.
         (assign, ":daily_restock", 120),
         (val_add, ":daily_restock", ":food_consumption"),
         (val_div, ":daily_restock", 2),

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

         # Safety: keep daily resupply bounded and non-negative.
         (val_clamp, ":daily_restock", 60, 481),

         (val_add, ":center_food_store", ":daily_restock"),
         (val_min, ":center_food_store", ":food_store_limit"),
         (party_set_slot, ":center_no", slot_party_food_store, ":center_food_store"),
       (try_end),
    ]),
]
