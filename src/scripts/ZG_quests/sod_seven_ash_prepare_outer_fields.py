SCRIPTS = [
("sod_seven_ash_prepare_outer_fields",
    [
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_siege_phase_active, sod_seven_ash_siege_phase_outer_fields),
      (quest_get_slot, ":host_strength", "qst_seven_ash_ultimatum", slot_quest_seven_ash_wulfred_host_strength),
      (quest_get_slot, ":pressure", "qst_seven_ash_ultimatum", slot_quest_seven_ash_wulfred_pressure),
      (quest_get_slot, ":intelligence", "qst_seven_ash_ultimatum", slot_quest_seven_ash_intelligence),
      (quest_get_slot, ":outer_sector", "qst_seven_ash_ultimatum", slot_quest_seven_ash_sector_outer_fields),

      # The outer fields are a screening phase: commit roughly one quarter of the
      # host, then let scouting and overcommitment change how much arrives fresh.
      (store_div, ":enemy_committed", ":host_strength", 4),
      (store_div, ":pressure_bonus", ":pressure", 5),
      (val_add, ":enemy_committed", ":pressure_bonus"),
      (store_div, ":scout_reduction", ":intelligence", 4),
      (val_sub, ":enemy_committed", ":scout_reduction"),
      (try_begin),
        (ge, ":outer_sector", 1),
        (val_sub, ":enemy_committed", 12),
      (try_end),
      (val_max, ":enemy_committed", 24),
      (val_min, ":enemy_committed", 80),

      (assign, ":wave_count", 2),
      (try_begin),
        (ge, ":enemy_committed", 54),
        (assign, ":wave_count", 3),
      (try_end),

      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_outer_enemy_committed, ":enemy_committed"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_outer_wave_count, ":wave_count"),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_outer_result, sod_seven_ash_siege_result_unresolved),
      (quest_set_slot, "qst_seven_ash_ultimatum", slot_quest_seven_ash_outer_casualty_pressure, 0),
      (assign, reg0, ":enemy_committed"),
      (assign, reg1, ":wave_count"),
  ]),
]
