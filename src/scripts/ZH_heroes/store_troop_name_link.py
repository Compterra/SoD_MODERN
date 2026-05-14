SCRIPTS = [
("store_troop_name_link",
	[
		(store_script_param_1, ":string"),
		(store_script_param_2, ":troop"),

	(try_begin),
		(neg|is_between, ":troop", 0, "trp_last_troop"),
		(str_store_string, ":string", "@an unknown commander"),
	(else_try),
		(str_store_troop_name_link, ":string", ":troop"),
	(try_end),
	]),
]
