DIALOGS = [
[anyone, "trainer_practice_1",
   [[eq, "$num_opponents_to_beat_in_a_row", 0], [eq, "$novice_training_difficulty", 2]],
 "You've got the heart of a champion, {lad/lass}, and the sword arm to match. From now on your opponents will be champion fighters.\
 These are the cream of the crop, the finest warriors I have trained. If you can best three of them in a row, you will join their ranks.",
   "trainer_practice_1",
   [[assign, "$num_opponents_to_beat_in_a_row", 3],
    [val_add, "$novice_training_difficulty", 1],
    [add_xp_to_troop, 100],
    [assign, "$novicemaster_opponent_troop", "trp_champion_fighter"]]],
]
