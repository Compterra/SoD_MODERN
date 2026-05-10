# -*- coding: cp1254 -*-

from src.constants.module_constants import *

SCRIPTS = [
("get_center_ideal_health",
        [
          (store_script_param, ":center_no", 1),
          (call_script, "script_sod_get_center_modifier_totals", ":center_no"),
          (assign, ":building_health_bonus", reg4),
          (call_script, "script_sod_get_center_population_capacity_profile", ":center_no"),
          (assign, ":population", reg0),
          (assign, ":effective_pop_ideal", reg7),
          (try_begin),
            (is_between, ":center_no", villages_begin, villages_end),
			(assign, ":ideal", 10),

            # land quality = -6..+9
            (party_get_slot, ":land_quality", ":center_no", slot_village_land_quality),
            (val_sub, ":ideal", 2), # -2..+3
            (val_mul, ":land_quality", 3), # 3 points per land quality
            (val_add, ":ideal", ":land_quality"),

            (val_add, ":ideal", ":building_health_bonus"),

            # population = -1 per 10 population outside of ideal
            (store_sub, ":crowding", ":effective_pop_ideal", ":population"),
            (val_div, ":crowding", 10),
            (val_add, ":ideal", ":crowding"),

          (else_try),
            (assign, ":ideal", 10),

            (val_add, ":ideal", ":building_health_bonus"),

            # population = -1 per 30 population outside of ideal
            (store_sub, ":crowding", ":effective_pop_ideal", ":population"),
            (val_div, ":crowding", 30),
            (val_add, ":ideal", ":crowding"),

          (try_end),
          (assign, reg0, ":ideal"),
        ]
      ),
]
