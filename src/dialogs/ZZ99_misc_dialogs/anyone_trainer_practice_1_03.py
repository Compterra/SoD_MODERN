DIALOGS = [
[anyone, "trainer_practice_1",
   [(eq, "$num_opponents_to_beat_in_a_row", 0), (eq, "$novice_training_difficulty", 0)],
 "Way to go {lad/lass}. With this victory, you have advanced to the next training level. From now on your opponents will be regular fighters, not the riff-raff off the street, so be on your toes.",
   "trainer_practice_1",
   [[assign, "$num_opponents_to_beat_in_a_row", 3],
    [val_add, "$novice_training_difficulty", 1],
    [add_xp_to_troop, 100],
    [assign, "$novicemaster_opponent_troop", "trp_regular_fighter"]]],
]
