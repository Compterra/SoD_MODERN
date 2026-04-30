from header_operations import *
from module_constants import *
from module_troops import *

try:
    slot_troop_companion_grievance
except NameError:
    slot_troop_companion_grievance = slot_troop_companion_cohesion + 1

COMPANION_COHESION_NEUTRAL = 50
COMPANION_COHESION_STRONG = 80
COMPANION_COHESION_WEAK = 20
COMPANION_GRIEVANCE_HIGH = 80
COMPANION_GRIEVANCE_LOW = 20

SCRIPTS = [
    ("companions_leave",
     [
         (store_script_param, ":maybe_target", 1),
         (store_script_param, ":base_pressure", 2),
         (assign, ":pressure", ":base_pressure"),
         (try_begin),
             (is_between, ":maybe_target", companions_begin, companions_end),
             (assign, ":troop_no", ":maybe_target"),
             (troop_get_slot, ":cohesion", ":troop_no", slot_troop_companion_cohesion),
             (troop_get_slot, ":grievance", ":troop_no", slot_troop_companion_grievance),
             (val_max, ":cohesion", 0),
             (val_min, ":cohesion", 100),
             (val_max, ":grievance", 0),
             (val_min, ":grievance", 100),

             (try_begin),
                 (ge, ":cohesion", COMPANION_COHESION_STRONG),
                 (val_sub, ":pressure", 20),
             (else_try),
                 (ge, ":cohesion", 65),
                 (val_sub, ":pressure", 12),
             (else_try),
                 (ge, ":cohesion", COMPANION_COHESION_NEUTRAL),
                 (val_sub, ":pressure", 5),
             (else_try),
                 (ge, ":cohesion", COMPANION_COHESION_WEAK),
                 (val_add, ":pressure", 8),
             (else_try),
                 (val_add, ":pressure", 15),
             (try_end),

             (try_begin),
                 (ge, ":grievance", COMPANION_GRIEVANCE_HIGH),
                 (val_add, ":pressure", 15),
             (else_try),
                 (ge, ":grievance", 50),
                 (val_add, ":pressure", 8),
             (else_try),
                 (lt, ":grievance", COMPANION_GRIEVANCE_LOW),
                 (val_add, ":pressure", 2),
             (try_end),

             (try_begin),
                 (gt, "$g_companion_recent_resentment", 40),
                 (val_add, ":pressure", 5),
             (try_end),
             (try_begin),
                 (gt, "$g_companion_clash_chain", 2),
                 (val_add, ":pressure", 3),
             (try_end),
         (else_try),
             (gt, ":maybe_target", 0),
             (assign, ":pressure", ":maybe_target"),
         (try_end),
         (assign, reg0, ":pressure"),
     ]),
]