from src.constants.module_constants import *

SCRIPTS = [
("get_center_ideal_prosperity",
        [(store_script_param, ":center_no", 1),
          (call_script, "script_sod_get_center_modifier_totals", ":center_no"),
          (assign, ":building_prosperity_cap_bonus", reg9),
          (store_sub, ":building_prosperity_multiplier_bonus", reg11, 100),
          (assign, ":ideal", 50),
          (try_begin),
            (is_between, ":center_no", villages_begin, villages_end),

            #MORDACHAI - consider the base value of the village as 40 + 3x land-quality
            (party_get_slot, ":land_quality", ":center_no", slot_village_land_quality),
            (val_mul, ":land_quality", 3),
            (val_add, ":ideal", ":land_quality"),

            (val_add, ":ideal", ":building_prosperity_cap_bonus"),

            #MORDACHAI - determine mill and manor improvement effects
            (assign, ":bonus", 100),

            (val_add, ":bonus", ":building_prosperity_multiplier_bonus"),

            #MORDACHAI - apply mill+manor bonus (if any)
            (val_mul, ":ideal", ":bonus"),
            (val_div, ":ideal", 100),

            #MORDACHAI - give an extra bonus based on cattle (1/20)
            (party_get_slot, ":num_cattle", ":center_no", slot_village_number_of_cattle),
            (val_div, ":num_cattle", 20),
            (val_add, ":ideal", ":num_cattle"),

          (else_try),
            #MORDACHAI - prosperity of castles & towns = 40 + (1/10th of each bound village - was 1/20th)
            (try_for_range, ":village_no", villages_begin, villages_end),
              (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
              (party_get_slot, ":prosperity", ":village_no", slot_town_prosperity),
              (val_div, ":prosperity", 10),
              (val_add, ":ideal", ":prosperity"),
            (try_end),

            (val_add, ":ideal", ":building_prosperity_cap_bonus"),

          (try_end),
          (assign, reg0, ":ideal"),
      ]),
]
