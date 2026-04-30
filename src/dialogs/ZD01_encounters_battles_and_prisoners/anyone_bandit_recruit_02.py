DIALOGS = [
[anyone, "bandit_recruit", [
      (store_encountered_party, ":party"),
      (store_party_size, ":size", ":party"),
      (store_mul, ":size", ":size", 50),
      (assign, reg0, ":size"),
   ], "we consider your offer for {reg0} denars", "bandit_recruit_2", []],
]
