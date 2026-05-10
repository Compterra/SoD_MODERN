SCRIPTS = [
("retire_companion",
        [
          (store_script_param_1, ":npc"),
          (store_script_param_2, ":length"),

          (call_script, "script_sod_companion_retinue_cleanup_for_departure", ":npc", sod_retinue_departure_peaceful),
          (remove_member_from_party, ":npc", "p_main_party"),
          (call_script, "script_sod_companion_cleanup_departed_companion", ":npc"),
          (troop_set_slot, ":npc", slot_troop_personalityclash_penalties, 0),
          (troop_set_slot, ":npc", slot_troop_morality_penalties, 0),
          (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
          (store_add, ":return_renown", ":renown", ":length"),
          (troop_set_slot, ":npc", slot_troop_occupation, slto_retirement),
          (troop_set_slot, ":npc", slot_troop_return_renown, ":return_renown"),
      ]),
]
