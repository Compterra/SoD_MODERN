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
    ("companions_join",
     [
         (store_script_param, ":maybe_target", 1),
         (store_script_param, ":base_score", 2),
         (assign, ":score", ":base_score"),
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
                 (val_add, ":score", 20),
             (else_try),
                 (ge, ":cohesion", 65),
                 (val_add, ":score", 10),
             (else_try),
                 (ge, ":cohesion", COMPANION_COHESION_NEUTRAL),
                 (val_add, ":score", 5),
             (else_try),
                 (ge, ":cohesion", COMPANION_COHESION_WEAK),
                 (val_sub, ":score", 5),
             (else_try),
                 (val_sub, ":score", 15),
             (try_end),

             (try_begin),
                 (ge, ":grievance", COMPANION_GRIEVANCE_HIGH),
                 (val_sub, ":score", 15),
             (else_try),
                 (ge, ":grievance", 50),
                 (val_sub, ":score", 8),
             (else_try),
                 (lt, ":grievance", COMPANION_GRIEVANCE_LOW),
                 (val_add, ":score", 3),
             (try_end),

             (try_begin),
                 (gt, "$g_companion_recent_resentment", 40),
                 (val_sub, ":score", 5),
             (try_end),
             (try_begin),
                 (gt, "$g_companion_clash_chain", 2),
                 (val_sub, ":score", 3),
             (try_end),
         (else_try),
             (gt, ":maybe_target", 0),
             (assign, ":score", ":maybe_target"),
         (try_end),
         (assign, reg0, ":score"),
     ]),
]