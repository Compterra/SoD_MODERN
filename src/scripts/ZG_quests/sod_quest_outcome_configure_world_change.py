SCRIPTS = [
("sod_quest_outcome_configure_world_change",
    [
      (store_script_param, ":quest_no", 1),
      (store_script_param, ":center_no", 2),
      (store_script_param, ":prosperity_delta", 3),
      (store_script_param, ":regional_instability_delta", 4),
      (store_script_param, ":lockout_days", 5),
      (quest_set_slot, ":quest_no", slot_quest_sod_reward_world_center, ":center_no"),
      (quest_set_slot, ":quest_no", slot_quest_sod_reward_world_prosperity, ":prosperity_delta"),
      (quest_set_slot, ":quest_no", slot_quest_sod_consequence_regional_instability, ":regional_instability_delta"),
      (quest_set_slot, ":quest_no", slot_quest_sod_consequence_lockout_days, ":lockout_days"),
      (quest_get_slot, ":flags", ":quest_no", slot_quest_sod_outcome_flags),
      (val_or, ":flags", sod_quest_outcome_flag_world_change),
      (val_or, ":flags", sod_quest_outcome_flag_consequence_configured),
      (quest_set_slot, ":quest_no", slot_quest_sod_outcome_flags, ":flags"),
  ]),
]
