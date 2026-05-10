SCRIPTS = [
("sod_seven_ash_mark_defender_resolved",
    [
      (store_script_param, ":defender_bit", 1),
      (store_script_param, ":terminal_state", 2),
      (quest_get_slot, ":resolved_count", "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_resolved_count),
      (quest_get_slot, ":recruited_bitmask", "qst_seven_ash_ultimatum", slot_quest_seven_ash_recruited_bitmask),
      (quest_get_slot, ":conflict_flags", "qst_seven_ash_ultimatum", slot_quest_seven_ash_defender_conflict_flags),

      (try_begin),
        (eq, ":terminal_state", sod_seven_ash_recruit_recruited),
        (val_or, ":recruited_bitmask", ":defender_bit"),
      (else_try),
        (this_or_next|eq, ":terminal_state", sod_seven_ash_recruit_alienated),
        (this_or_next|eq, ":terminal_state", sod_seven_ash_recruit_lost),
        (eq, ":terminal_state", sod_seven_ash_recruit_abandoned),
        (val_or, ":conflict_flags", ":defender_bit"),
      (try_end),

      (val_add, ":resolved_count", 1),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_resolved_count, ":resolved_count"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_recruited_bitmask, ":recruited_bitmask"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_defender_conflict_flags, ":conflict_flags"),

      (try_begin),
        (ge, ":resolved_count", 7),
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_act2_complete, 1),
        (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_active_stage, sod_seven_ash_stage_return),
      (try_end),
  ]),
]
