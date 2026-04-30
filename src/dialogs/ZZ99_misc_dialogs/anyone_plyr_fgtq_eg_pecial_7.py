DIALOGS = [
[anyone|plyr, "fgtq_eg_pecial_7", [
  ], "Very well, priestess. I'll ready my soldiers and give the sign when we may begin.", "close_window", [
	(assign, ":fgtq_mt", "mt_fgtq_inf"),
	(assign, ":fgtq_scene", "scn_fgtq_eg_s3"),
	(modify_visitors_at_site, ":fgtq_scene"),
	(reset_visitors),
	(call_script, "script_fgtq_add_player_troops_to_scene", 8),
	(try_for_range, ":entry_p", 10, 19),
		(set_visitor, ":entry_p", "trp_elephant_guard_battle_shaman"),
	(try_end),
	(set_visitor, 0, "trp_player"),
    (set_jump_mission, ":fgtq_mt"),
    (jump_to_scene, ":fgtq_scene"),
	(change_screen_mission),
  ] ],
]
