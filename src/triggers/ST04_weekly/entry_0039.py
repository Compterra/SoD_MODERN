SIMPLE_TRIGGERS = [
(24 * 7,
    [
      # Adding earnings to town lords' wealths and local operating treasuries from real taxes.
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
        (neq, ":town_lord", "trp_player"),
        (is_between, ":town_lord", kingdom_heroes_begin, kingdom_heroes_end),
        (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
        (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
        (troop_get_slot, ":troop_wealth", ":town_lord", slot_troop_wealth),
        (party_get_slot, ":center_wealth", ":center_no", slot_town_wealth),

        # Safety: these are money amounts; never allow negative values to corrupt NPC wealth.
        (val_max, ":accumulated_rents", 0),
        (val_max, ":accumulated_tariffs", 0),
        (val_max, ":troop_wealth", 0),
        (val_max, ":center_wealth", 0),

        (assign, ":total_income", ":accumulated_rents"),
        (val_add, ":total_income", ":accumulated_tariffs"),

        # Keep a real local reserve so the center has operating funds for upkeep and war recovery.
        (assign, ":center_reserve", ":total_income"),
        (val_div, ":center_reserve", 5),
        (assign, ":lord_income", ":total_income"),
        (val_sub, ":lord_income", ":center_reserve"),

        (val_add, ":troop_wealth", ":lord_income"),
        (val_add, ":center_wealth", ":center_reserve"),

        # Safety: keep finances within reasonable integer bounds.
        (val_min, ":troop_wealth", 2000000),
        (val_min, ":center_wealth", 2000000),

        (troop_set_slot, ":town_lord", slot_troop_wealth, ":troop_wealth"),
        (party_set_slot, ":center_no", slot_town_wealth, ":center_wealth"),
        (party_set_slot, ":center_no", slot_center_accumulated_rents, 0),
        (party_set_slot, ":center_no", slot_center_accumulated_tariffs, 0),
        (try_begin),
          (eq, "$cheat_mode", 1),
          (assign, reg1, ":troop_wealth"),
          (add_troop_note_from_sreg, ":town_lord", 1, "@Current wealth: {reg1}", 0),
        (try_end),
      (try_end),
    ]),
]
