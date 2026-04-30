SIMPLE_TRIGGERS = [
(24,
  [
    # we're invested
    (eq, "$g_sod_invested", 1),

    # and we're not a prisoner...
    (neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 0),

    # check if our investment has come due
    (store_current_day, ":cur_day"),
    (ge, ":cur_day", "$g_sod_invested_day"),
    (jump_to_menu, "mnu_investment_report"),
  ]),
]
