from header_common import *
from header_operations import *
from src.constants.module_constants import *


# COST: O(1), defensive validation before formal lord duel missions.
SCRIPTS = [
("cf_sod_valid_lord_duel_target",
 [
   (store_script_param_1, ":troop_no"),
   (is_between, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
   (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
   (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_dead),
   (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
   (neg|is_between, ":troop_no", pretenders_begin, pretenders_end),
 ]),
]
