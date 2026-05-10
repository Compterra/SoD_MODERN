SCRIPTS = [
("store_troop_name",
	[
		(store_script_param_1, ":string"),
		(store_script_param_2, ":troop"),

	(try_begin),
		(neg|is_between, ":troop", 0, "trp_last_troop"),
		(str_store_string, ":string", "@unknown captain"),
	(else_try),
		(troop_get_slot, ":title", ":troop", slot_troop_title),
		(is_between, ":title", "str_sod_c1_ruler", "str_bc_random_warrior1_1"),
		(str_store_troop_name, s37, ":troop"),
		(str_store_string, s27, ":title"),
		(str_store_string, ":string", "@{s27} {s37}"),
	(else_try),
		(str_store_troop_name, ":string", ":troop"),
	(try_end),
	]),
]
