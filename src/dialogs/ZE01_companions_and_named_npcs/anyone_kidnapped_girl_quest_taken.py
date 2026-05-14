DIALOGS = [
[anyone, "kidnapped_girl_quest_taken", [
      (try_begin),
        (eq, "$g_sod_last_rescue_spawn_ok", 1),
        (str_store_string, s2, "@Good. I knew we could trust you at this.\
 Here is the ransom money, {reg12} denars.\
 Count it before taking it.\
 And please, don't attempt to do anything rash.\
 Keep in mind that the girl's well being is more important than anything else..."),
      (else_try),
        (str_store_string, s2, "@The bandits' trail has gone cold. I cannot send you out with ransom money until we know where they are. Come back later and we will try again."),
      (try_end),
      ], "{s2}", "close_window",
   []],
]
