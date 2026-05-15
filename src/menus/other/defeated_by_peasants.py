MENUS = [
("defeated_by_peasants", mnf_disable_all_keys,
	"The peasants hold the village. Your company is driven back before the fires can take.",
	"none",
	[
	(try_begin),
	  (check_quest_active, "qst_slavers_deal_with_good_guys"),
	  (quest_slot_eq, "qst_slavers_deal_with_good_guys", slot_quest_target_center, "$current_town"),
	  (call_script, "script_fail_quest", "qst_slavers_deal_with_good_guys"),
	  (call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_retreat_or_fail, 1),
	(try_end),
	],
	[
	("continue", [], "Continue...",
	[(change_screen_map),]),
	]),
]
