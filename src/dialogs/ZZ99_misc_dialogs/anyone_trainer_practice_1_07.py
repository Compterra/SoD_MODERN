DIALOGS = [
[anyone, "trainer_practice_1",
   [
     (assign, reg8, "$num_opponents_to_beat_in_a_row"),
     (call_script, "script_store_troop_name", s9, "$novicemaster_opponent_troop"),
     ],
 "Your next opponent will be a {s9}. You need to win {reg8} more\
 fights in a row to advance to the next stage. Are you ready?", "novicemaster_are_you_ready",
   []],
]
