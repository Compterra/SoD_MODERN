SCRIPTS = [
("sod_seven_ash_begin_act3_return",
    [
      (try_begin),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_complete, 1),
        (quest_slot_eq, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act3_pressure_started, 0),

        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act3_pressure_started, 1),
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_pressure),
        (quest_get_slot, ":pressure", "qst_seven_ash_ultimatum", slot_quest_seven_ash_wulfred_pressure),
        (val_add, ":pressure", 10),
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_wulfred_pressure, ":pressure"),

        (str_store_string, s49, "@The recruitment road is over. Mother Hilda counts beds, Reeve Martin counts food and days, and Nell watches the road behind the player. Ashwick has entered the pressure before Wulfred's host arrives."),
        (add_quest_note_from_sreg, "qst_seven_ash_return_to_ashwick", 2, s49, 0),
        (call_script, "script_sod_quest_chain_branch_success", "qst_seven_ash_return_to_ashwick", "qst_seven_ash_pressure_interlude", 0),
      (try_end),
  ]),
]
