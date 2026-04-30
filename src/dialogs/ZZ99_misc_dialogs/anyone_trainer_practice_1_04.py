DIALOGS = [
[anyone, "trainer_practice_1",
   [[eq, "$num_opponents_to_beat_in_a_row", 0], [eq, "$novice_training_difficulty", 1]],
 "Way to go {lad/lass}. Welcome to the third training level. From now on your opponents will be veteran fighters; soldiers and arena regulars and the like. These guys know some dirty tricks, so keep your defense up.",
   "trainer_practice_1",
   [[assign, "$num_opponents_to_beat_in_a_row", 3],
    [val_add, "$novice_training_difficulty", 1],
    [add_xp_to_troop, 100],
    [assign, "$novicemaster_opponent_troop", "trp_veteran_fighter"]]],
]
