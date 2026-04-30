from header_operations import *
from module_constants import *
from module_troops import *

try:
    slot_troop_companion_grievance
except NameError:
    slot_troop_companion_grievance = slot_troop_companion_cohesion + 1

COMPANION_COHESION_NEUTRAL = 50

SCRIPTS = [
    ("companions_validate",
     [
         (store_script_param, ":maybe_target", 1),
         (assign, ":corrections", 0),
         (try_begin),
             (is_between, ":maybe_target", companions_begin, companions_end),
             (assign, ":troop_no", ":maybe_target"),
             (troop_get_slot, ":cohesion", ":troop_no", slot_troop_companion_cohesion),
             (troop_get_slot, ":grievance", ":troop_no", slot_troop_companion_grievance),
             (assign, ":clamped_cohesion", ":cohesion"),
             (assign, ":clamped_grievance", ":grievance"),
             (val_max, ":clamped_cohesion", 0),
             (val_min, ":clamped_cohesion", 100),
             (val_max, ":clamped_grievance", 0),
             (val_min, ":clamped_grievance", 100),
             (try_begin),
                 (neq, ":clamped_cohesion", ":cohesion"),
                 (troop_set_slot, ":troop_no", slot_troop_companion_cohesion, ":clamped_cohesion"),
                 (val_add, ":corrections", 1),
             (try_end),
             (try_begin),
                 (neq, ":clamped_grievance", ":grievance"),
                 (troop_set_slot, ":troop_no", slot_troop_companion_grievance, ":clamped_grievance"),
                 (val_add, ":corrections", 1),
             (try_end),
         (else_try),
             (try_for_range, ":troop_no", companions_begin, companions_end),
                 (troop_get_slot, ":cohesion", ":troop_no", slot_troop_companion_cohesion),
                 (troop_get_slot, ":grievance", ":troop_no", slot_troop_companion_grievance),
                 (assign, ":clamped_cohesion", ":cohesion"),
                 (assign, ":clamped_grievance", ":grievance"),
                 (val_max, ":clamped_cohesion", 0),
                 (val_min, ":clamped_cohesion", 100),
                 (val_max, ":clamped_grievance", 0),
                 (val_min, ":clamped_grievance", 100),
                 (try_begin),
                     (neq, ":clamped_cohesion", ":cohesion"),
                     (troop_set_slot, ":troop_no", slot_troop_companion_cohesion, ":clamped_cohesion"),
                     (val_add, ":corrections", 1),
                 (try_end),
                 (try_begin),
                     (neq, ":clamped_grievance", ":grievance"),
                     (troop_set_slot, ":troop_no", slot_troop_companion_grievance, ":clamped_grievance"),
                     (val_add, ":corrections", 1),
                 (try_end),
             (try_end),
         (try_end),
         (assign, reg0, ":corrections"),
     ]),
]