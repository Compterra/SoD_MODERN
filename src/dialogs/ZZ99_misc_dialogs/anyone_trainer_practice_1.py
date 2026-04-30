DIALOGS = [
[anyone, "trainer_practice_1", [(eq, "$training_system_explained", 0)],
 "I train novices in four stages, each tougher than the one before.\
 To finish a stage and advance to the next one, you have to win three fights in a row.", "trainer_practice_1",
   [
     (assign, "$num_opponents_to_beat_in_a_row", 3),
     (assign, "$novicemaster_opponent_troop", "trp_novice_fighter"),
     (assign, "$training_system_explained", 1),
     ]],
]
