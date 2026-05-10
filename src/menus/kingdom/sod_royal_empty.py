MENUS = [
("sod_royal_empty", 0,
	"My liege. {s22} heroes returned from the expedition. They found sealed ledgers and local testimony proving this region holds no royal artifact. We can cross it from the search.",
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
