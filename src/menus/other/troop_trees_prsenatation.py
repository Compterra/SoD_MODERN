MENUS = [
("troop_trees_prsenatation", 0,
	"Strategy advisor pulls a book from his sack.",
	"none", [
	],
	[
	("continue",[],"Continue...",[
	(jump_to_menu, "mnu_troop_trees_prsenatation_end"),
	(start_presentation, "prsnt_sod_troop_trees"),
	]),
	("back",[],"Resume travelling.",[
	(change_screen_return),
	]),
	],),
]
