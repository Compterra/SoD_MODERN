DIALOGS = [
[anyone, "prison_break_2_accepted", [
  (setup_quest_text, "qst_slave_q3"),
  (str_store_string, s2, "@Fight your way out of the dungeon."),
  (call_script, "script_start_quest", "qst_slave_q3", "$g_talk_troop"),
  ], "Excellent ! I'll be finally out of this den of evil ! Once you freed me, get me that big club on the wall. Oh, I will enjoy hearing the sound of shattering Slaver skulls. I have survived their hellish fighting pits for years; they are no match for the two of us ! Come, let's get out of here ! We shall leave nothing behind but a trail of rotten carcasses - a fitting punishment for the crimes they committed !", "close_window", [
  (assign, "$prison_break", 5),
  
	(modify_visitors_at_site, "scn_prison_break"),
	(reset_visitors),
	
	(set_visitor, 0, "trp_player"),
	(set_visitor, 1, "trp_slave_hero"),
	
	(set_visitor, 10, "trp_tormenter"),
	(set_visitor, 11, "trp_slave_hunter"),
	(set_visitor, 12, "trp_henchman"),
	(set_visitor, 13, "trp_slave_crusher"),
	(set_visitor, 14, "trp_slave_driver"),
	
    (set_jump_mission, "mt_prison_break"),
    (jump_to_scene, "scn_prison_break"),
	(change_screen_mission),
	
  ]],
]
