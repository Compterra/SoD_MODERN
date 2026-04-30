MENUS = [
("sod_royal_location", 0,
	"Good news, my liege. {s22} heroes returned with a hard lead: the artifact is there. They found the trail, but the final chamber was too guarded to breach. A second expedition to the same site should press the advantage.",
	"none", [
	(call_script, "script_sod_royal_return_expedition_heroes", 0),
	],
	[
	("continue",[],"Continue...",[
	(assign, "$sod_royal_cur_mission", 0),
	(assign, "$sod_royal_heroes", 0), #twan456
	(change_screen_return),
	]),
	]),
]
