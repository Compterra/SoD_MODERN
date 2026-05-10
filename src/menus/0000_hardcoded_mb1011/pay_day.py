MENUS = [
(
    "pay_day", mnf_scale_picture|mnf_disable_all_keys,
    "{s10}",
    "none",
    [
        (set_background_mesh, "mesh_pic_payment"),

        # get the player's current wealth before income & wages
        (store_troop_gold, ":player_wealth", "trp_player"),
        (assign, ":original_wealth", ":player_wealth"),

        # MORDACHAI - Kings get their taxes and pay all of their debts here, at once (its good to be the King)
        (try_begin),
          (eq, "$g_sod_king", 1),

          # generate expense report for past week
          (assign, reg0, "$g_sod_weekly_troops_hired"),
          (assign, reg1, "$g_sod_weekly_troops_upgraded"),
          (assign, reg2, "$g_sod_weekly_construction"),
          (str_store_string, s10, "@Over the past week you have spent {reg0?{reg0} hiring new troops, :}{reg1?{reg1} upgrading troops, :}{reg2?{reg2} for construction projects,:}"),
          (store_sub, reg3, ":original_wealth", "$g_sod_weekly_starting_cash"),
          (try_begin),
            (gt, reg3, 0),
            (str_store_string, s10, "@{s10} but you gained {reg3} denars during your week's exploits."),
          (else_try),
            (lt, reg3, 0),
            (val_abs, reg3),
            (str_store_string, s10, "@{s10} and another {reg3} on everything else."),
          (else_try),
            (eq, reg3, 0),
            (str_store_string, s10, "@{s10} but you broke even on everything else."),
          (try_end),

          # collect all taxes at once
          (assign, ":total_income", 0),
          (try_for_range, ":center_no", centers_begin, centers_end),
            (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
            (neq, "$g_sod_player_tax_couriers_enabled", 1),
            (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
            (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
            # Safety: never allow negative stored totals to poison payday.
            (val_max, ":accumulated_rents", 0),
            (val_max, ":accumulated_tariffs", 0),
            (val_add, ":total_income", ":accumulated_rents"),
            (val_add, ":total_income", ":accumulated_tariffs"),
            (party_set_slot, ":center_no", slot_center_accumulated_rents, 0),
            (party_set_slot, ":center_no", slot_center_accumulated_tariffs, 0),
          (try_end),
		  
		  #Economic difficulty
		  (try_begin),
			(eq, "$g_sod_difficulty", -1),
			(val_mul, ":total_income", 3),
			(val_div, ":total_income", 2),
		  (else_try),
			(eq, "$g_sod_difficulty", 1),
			(val_div, ":total_income", 2),
		  (try_end),
		  
          (assign, reg1, ":total_income"),
		  (try_begin),
			(gt, "$g_sod_weekly_scoutage", 0),
			(val_add, ":total_income", "$g_sod_weekly_scoutage"),
			(assign, reg0, "$g_sod_weekly_scoutage"),
			(str_store_string, s20, "@Royal Tribute: {reg0} denars^"),
		  (else_try),
			(str_clear, s20),
		  (try_end),
		  (assign, "$g_sod_weekly_scoutage", 0),

          # Safety: income should never go negative (can break later wage math).
          (val_max, ":total_income", 0),

          (str_store_string, s10, "@{s10}^^Today you receive the accumulated rents and taxes of your fiefs, amounting to {reg1} denars. "),
          (str_store_string, s20, "@Tax Income: {reg1} denars^{s20}"),
        (else_try),
          (assign, ":total_income", 0),
          (str_clear, s10),
          (str_clear, s20),
        (try_end),

        # determine total wages
        # Safety: avoid divide-by-zero and negative wages.
        (val_max, "$g_sod_wages", 0),
        (val_max, "$g_sod_times_wages_added", 1),
        (store_div, ":total_wages", "$g_sod_wages", "$g_sod_times_wages_added"),
		(assign, "$g_sod_wages", 0),
		(assign, "$g_sod_times_wages_added", 0),
        (call_script, "script_sod_companion_retinue_pay_weekly_wages"),
        (assign, reg9, reg0),
        (assign, reg10, reg1),
        (assign, reg11, reg2),
        (assign, reg12, reg3),
        (assign, reg13, reg4),
        (try_begin),
          (gt, reg10, 0),
          (val_sub, ":total_wages", reg10),
          (val_add, ":total_wages", reg12),
          (val_max, ":total_wages", 0),
          (str_store_string, s20, "@{s20}Companion command cost: {reg10} denars^{reg9?Command purses paid {reg9} denars^:}{reg12?Retinue shortages covered by this wage bill: {reg12} denars^:}{reg13?Unpaid retinue shortages: {reg13} denars^:}"),
        (try_end),

        # determine total debt to troops SoD - Kuba: small fix, add -> sub
        # Safety: debt should never be negative when used here.
        (val_max, "$g_player_debt_to_party_members", 0),
        (store_sub, ":total_debt", ":total_wages", "$g_player_debt_to_party_members"),

        # determine the net change in wealth (and the resulting total wealth)
        (store_sub, ":net_change", ":total_income", ":total_debt"),
        (val_add, ":player_wealth", ":net_change"),

        (assign, reg2, "$g_player_debt_to_party_members"),
        (assign, reg3, ":total_debt"),
        (store_add, reg4, ":original_wealth", ":total_income"),
        (assign, reg5, ":player_wealth"),
        (assign, reg6, ":total_wages"),
        (assign, reg7, ":net_change"),
        (val_abs, reg7),

        (try_begin),
          # check if we're in the black
          (ge, ":player_wealth", 0),
          (assign, "$g_player_debt_to_party_members", 0),
          (str_store_string, s10, "@{s10}You paid {reg3} of your {reg4} denars to your men. You have {reg5} denars left.^^"),
          # add or subtract the net amount
          (try_begin),
            (gt, ":net_change", 0),
            (play_sound, "snd_money_received"),
            (troop_add_gold, "trp_player", ":net_change"),
          (else_try),
            (lt, ":net_change", 0),
            (play_sound, "snd_money_paid"),
            (store_mul, ":paid", ":net_change", -1), # invert the sign
            (call_script, "script_sod_player_charge_gold", ":paid"), # charge the player's account for the net amount
          (try_end),
        (else_try),
          # we're in the red
          (call_script, "script_sod_player_charge_gold", ":original_wealth"), # wipe the player's bank out
          (play_sound, "snd_money_paid"),
          # :player_wealth is negative here; convert to a positive unpaid amount.
          (store_mul, ":unpaid", ":player_wealth", -1),
          (val_max, ":unpaid", 0),
          (val_min, ":unpaid", 2000000),
          (assign, reg8, ":unpaid"),
          (str_store_string, s10, "@{s10}Your debt to your men amounted to {reg3} denars, however you only had {reg4}. Unpaid sum of {reg8} denars is added as debt. Your party loses morale.^^"),
          (assign, "$g_player_debt_to_party_members", ":unpaid"),
          (store_div, ":unpaid_weight", ":unpaid", 500),
          (val_add, ":unpaid_weight", 1),
          (val_clamp, ":unpaid_weight", 1, 8),
          (call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_unpaid_wages, ":unpaid_weight"),
          (call_script, "script_sod_companion_try_bunduk_line_incident", 2, ":unpaid_weight"),
          (call_script, "script_sod_companion_try_katrin_last_coin_incident", 2, ":unpaid_weight"),
          (call_script, "script_objectionable_action", tmt_egalitarian, "str_men_unpaid"),
        (try_end),

        # reg0 = was a net gain (1), or loss (0)
        (try_begin),
          (ge, ":net_change", 0),
          (assign, reg0, 1),
        (else_try),
          (assign, reg0, 0),
        (try_end),

        # give them the details
        (assign, reg8, ":original_wealth"),
        (str_store_string, s10, "@{s10}Previous wealth: {reg8} denars^{s20}This week's wages: {reg6} denars^Earlier debts: {reg2} denars^{reg0?Net income:Total payment}: {reg7} denars^Current wealth: {reg5} denars"),

        (try_begin),
          (eq, "$g_sod_king", 1),
          # go ahead and reset the weekly accumulators
          (store_troop_gold, "$g_sod_weekly_starting_cash", "trp_player"),
          (assign, "$g_sod_weekly_troops_hired", 0),
          (assign, "$g_sod_weekly_troops_upgraded", 0),
          (assign, "$g_sod_weekly_construction", 0),
        (try_end),
    ],
    [
      ("continue", [], "Continue...", [(change_screen_return, 0)]),
    ]
  ),
]
