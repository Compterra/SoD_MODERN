SCRIPTS = [
("calculate_hero_weekly_net_income_and_add_to_wealth",
    [
      (store_script_param_1, ":troop_no"),

      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),

      (troop_get_slot, ":cur_debt", ":troop_no", slot_troop_player_debt),
      (val_mul, ":cur_debt", 101),
      (val_div, ":cur_debt", 100),
      (troop_set_slot, ":troop_no", slot_troop_player_debt, ":cur_debt"),

      (assign, ":weekly_outgo", 0),
      (try_begin),
        (gt, ":party_no", 0),
        (call_script, "script_calculate_weekly_party_wage", ":party_no"),
        (assign, ":weekly_outgo", reg0),
      (try_end),

      # Lords now rely on real tax income from their centers.
      # This script only applies weekly upkeep pressure to their personal wealth.
      (val_sub, ":cur_wealth", ":weekly_outgo"),
      (val_max, ":cur_wealth", 0),
      (troop_set_slot, ":troop_no", slot_troop_wealth, ":cur_wealth"),
  ]),
]
