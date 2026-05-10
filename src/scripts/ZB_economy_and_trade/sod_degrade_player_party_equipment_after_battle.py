SCRIPTS = [
("sod_degrade_player_party_equipment_after_battle",
 [
   (assign, ":total_damaged", 0),
   (assign, ":wear_chance", 4),

   (call_script, "script_sod_degrade_troop_equipped_items_after_battle", "trp_player", ":wear_chance"),
   (val_add, ":total_damaged", reg0),

   (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
   (try_for_range, ":stack_no", 0, ":num_stacks"),
     (party_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
     (is_between, ":troop_no", companions_begin, companions_end),
     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_player_companion),
     (call_script, "script_sod_degrade_troop_equipped_items_after_battle", ":troop_no", ":wear_chance"),
     (val_add, ":total_damaged", reg0),
   (try_end),

   (assign, reg0, ":total_damaged"),
   (try_begin),
     (gt, ":total_damaged", 0),
     (assign, reg21, ":total_damaged"),
     (display_message, "@Battle wear damaged {reg21} equipped item(s). Visit a smith, armorer, or stable to repair them.", 0xFFCC66),
   (try_end),
 ]),
]
