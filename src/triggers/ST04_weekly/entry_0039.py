SIMPLE_TRIGGERS = [
(24 * 7,
    [
      # Adding earnings to town lords' wealths and local operating treasuries from real taxes.
      # Tax courier dispatch now physicalizes part of eligible NPC lord income.
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
        (try_begin),
          (eq, ":town_lord", "trp_player"),
          (call_script, "script_sod_try_dispatch_player_tax_courier_from_center", ":center_no"),
        (else_try),
          (is_between, ":town_lord", kingdom_heroes_begin, kingdom_heroes_end),
          (call_script, "script_sod_try_dispatch_ai_tax_courier_from_center", ":center_no"),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (troop_get_slot, ":troop_wealth", ":town_lord", slot_troop_wealth),
            (assign, reg1, ":troop_wealth"),
            (str_store_string, s49, "@Current wealth: {reg1}"),

            (add_troop_note_from_sreg, ":town_lord", 1, s49, 0),
          (try_end),
        (try_end),
      (try_end),
    ]),
]
