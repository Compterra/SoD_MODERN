DIALOGS = [
[anyone, "novicemaster_ready_to_fight", [], "Here you go then. Good luck.", "close_window",
   [
     (assign, "$training_fight_won", 0),
     (assign, "$waiting_for_training_fight_result", 1),
     (modify_visitors_at_site, "$g_training_ground_melee_training_scene"),
     (reset_visitors),
     (assign, reg0, 0),
     (assign, reg1, 1),
     (assign, reg2, 2),
     (assign, reg3, 3),
     (shuffle_range, 0, 4),
     (set_visitor, reg0, "trp_player"),
     (set_visitor, reg1, "$novicemaster_opponent_troop"),
     (set_visitor, 4, "$g_talk_troop"),
     (set_jump_mission, "mt_training_ground_trainer_training"),
     (jump_to_scene, "$g_training_ground_melee_training_scene"),
     ]],
]
