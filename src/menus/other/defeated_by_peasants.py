MENUS = [
("defeated_by_peasants", mnf_disable_all_keys,
	"The peasants defended their village",
	"none",
	[
	(call_script, "script_fail_quest", "qst_slavers_deal_with_good_guys"),
	],
	[
	("continue", [], "Continue...",
	[(change_screen_map),]),
	]),
]
