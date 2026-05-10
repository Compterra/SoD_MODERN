from header_common import *
from header_operations import *
from src.constants.module_constants import *

# COST: O(number of kingdom heroes), only called when a player-kingdom campaign is explicitly summoned.


SCRIPTS = [
("sod_player_kingdom_summon_marshal_campaign",
    [
      (store_script_param_1, ":faction_no"),

      (assign, ":summoned_count", 0),
      (assign, ":marshal_party", -1),
      (faction_get_slot, ":marshal_no", ":faction_no", slot_faction_marshall),
      (try_begin),
        (eq, ":marshal_no", "trp_player"),
        (assign, ":marshal_party", "p_main_party"),
      (else_try),
        (is_between, ":marshal_no", kingdom_heroes_begin, kingdom_heroes_end),
        (troop_get_slot, ":marshal_party", ":marshal_no", slot_troop_leaded_party),
        (try_begin),
          (gt, ":marshal_party", 0),
          (neg|party_is_active, ":marshal_party"),
          (assign, ":marshal_party", -1),
        (try_end),
      (try_end),

      (try_begin),
        (ge, ":marshal_party", 0),
        (try_for_range, ":lord_no", kingdom_heroes_begin, kingdom_heroes_end),
          (neq, ":lord_no", ":marshal_no"),
          (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
          (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
          (store_troop_faction, ":lord_faction", ":lord_no"),
          (eq, ":lord_faction", ":faction_no"),
          (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
          (gt, ":lord_party", 0),
          (party_is_active, ":lord_party"),
          (party_get_battle_opponent, ":battle_opponent", ":lord_party"),
          (lt, ":battle_opponent", 0),
          (troop_get_slot, ":readiness", ":lord_no", slot_troop_readiness_to_join_army),
          (val_max, ":readiness", 65),
          (troop_set_slot, ":lord_no", slot_troop_readiness_to_join_army, ":readiness"),
          (troop_set_slot, ":lord_no", slot_troop_readiness_to_follow_orders, ":readiness"),
          (troop_set_slot, ":lord_no", slot_troop_player_order_state, spai_accompanying_army),
          (troop_set_slot, ":lord_no", slot_troop_player_order_object, ":marshal_party"),
          (party_set_slot, ":lord_party", slot_party_commander_party, ":marshal_party"),
          (call_script, "script_party_set_ai_state", ":lord_party", spai_accompanying_army, ":marshal_party"),
          (call_script, "script_sod_lord_update_strategic_intent", ":lord_no"),
          (val_add, ":summoned_count", 1),
        (try_end),
      (try_end),

      (try_begin),
        (eq, "$g_sod_debug", 1),
        (assign, reg20, ":summoned_count"),
        (str_store_faction_name, s20, ":faction_no"),
        (display_log_message, "@marshal_campaign_summon: {s20} assigned {reg20} lords to the marshal.", debug_color),
      (try_end),

      (assign, reg0, ":summoned_count"),
  ]),
]
