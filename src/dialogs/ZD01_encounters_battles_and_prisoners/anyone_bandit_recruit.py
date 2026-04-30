DIALOGS = [
[anyone, "bandit_recruit", [
      (store_random_in_range, ":rand", -5, 16),
      (gt, "$player_honor", ":rand"),
   ], "A {boy/girl} like you, who could do no misdeeds? Heck no. We will slit your throat for your impudence!", "close_window", [encounter_attack]],
]
