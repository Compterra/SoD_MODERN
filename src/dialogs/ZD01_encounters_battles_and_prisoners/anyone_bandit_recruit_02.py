DIALOGS = [
[anyone, "bandit_recruit", [
      (store_encountered_party, ":party"),
      (store_party_size, ":size", ":party"),
      (store_mul, ":size", ":size", 50),
      (assign, reg0, ":size"),
   ], "For {reg0} denars, we might pretend your banner was our idea all along.", "bandit_recruit_2", []],
]
