DIALOGS = [
[anyone, "start", [
  (ge, "$fight_guild_troops_quest", 2),
  (eq, "$fgtq_state", fgtq_sh_2_next),
  (str_store_string_reg, s68, s1),
  ], "{s68}", "close_window", [
	(assign, ":fgtq_mt", "mt_fgtq_cav"),
	(assign, ":fgtq_scene", "scn_fgtq_sh_s4"),
	(modify_visitors_at_site, ":fgtq_scene"),
	(reset_visitors),
	(set_visitor, 10, "trp_serpent_host_basilisk_knight"),
	(set_visitor, 11, "trp_serpent_host_basilisk_knight"),
	(set_visitor, 0, "trp_player"),
    (set_jump_mission, ":fgtq_mt"),
    (jump_to_scene, ":fgtq_scene"),
	(change_screen_mission),
  ] ],
]
