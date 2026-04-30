MENUS = [
("sod_royal_failure", 0,
	"My liege. {s22} heroes returned from the expedition. They searched ruins, vaults, and occupied halls, but found no firm proof. The artifact may still be hidden there.^{s21}",
	"none", [
	(call_script, "script_sod_royal_return_expedition_heroes", 0),
	],
	[
	("continue",[],"Continue...",[
	(assign, "$sod_royal_cur_mission", 0),
	(assign, "$sod_royal_heroes", 0), #twan456
	(change_screen_return),
	]),
	],),
]
