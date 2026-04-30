DIALOGS = [
[anyone , "arena_master_fight_result", [(assign, reg10, arena_grand_prize)],
   "Congratulations champion! Your fight there was something to remember! You managed to be the last fighter standing beating down everyone else. And of course you won the grand prize of the fights: {reg10} denars.", "arena_master_pre_talk", [
     (call_script, "script_troop_add_gold", "trp_player", arena_grand_prize),
     (add_xp_to_troop, 200, "trp_player"),
     (assign, "$last_training_fight_town", -1)]],
]
