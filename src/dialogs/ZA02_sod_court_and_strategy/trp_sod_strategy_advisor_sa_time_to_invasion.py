DIALOGS = [
[trp_sod_strategy_advisor, "sa_time_to_invasion", [
	(store_mul, reg1, "$g_sod_invasion_begin", "$g_sod_invasion_inaccuracy"),
	(val_div, reg1, 100),
    (store_current_day, ":today"),
    (store_sub, reg2, reg1, ":today"),
    (try_begin),
      (lt, ":today", "$g_sod_invasion_begin"),
      (str_store_string, s1, "@My spies tell me the Legion will invade Calradia around day {reg1}.  This gives you approximately {reg2} days to prepare.  Be wary though my lord, The Legion could be supplying false dates purposely for the element of surprise.  Let us prepare today and conquer this dam continent and give them hell when they arrive."),
      (assign, reg9, 0),
    (else_try),
      (str_store_string, s1, "@It has already begun!"),
      (assign, reg9, 1),
    (try_end),
	], "{s1}", "sa_select_3_answer", []],
]
