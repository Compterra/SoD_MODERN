SIMPLE_TRIGGERS = [
(12,
   [
     (call_script, "script_calculate_player_faction_wage"),
	 # Safety: wages should be a non-negative amount.
	 (val_max, reg0, 0),
	 (val_add, "$g_sod_wages", reg0),
	 (val_clamp, "$g_sod_wages", 0, 2000001),
	 (val_add, "$g_sod_times_wages_added", 1),
	 (val_clamp, "$g_sod_times_wages_added", 0, 1000),
	 (try_begin),
		(ge, "$g_sod_times_wages_added", 14),
		(assign, "$g_cur_week_half_daily_wage_payments", 0), #Reseting the weekly half wage payments
		(jump_to_menu, "mnu_pay_day"),
	 (try_end),
    ]),
]
