DIALOGS = [
[anyone, "bandit_attack", [
      (store_random_in_range, ":rand", 11, 15),
        (str_store_string, s11, "@Another fool come to throw {him/her}self on my weapon, eh? Fine, let's fight!"),
        (str_store_string, s12, "@We're not afraid of you, {sirrah/wench}. Time to bust some heads!"),
        (str_store_string, s13, "@That was a mistake. Now I'm going to have to make your death long and painful."),
        (str_store_string, s14, "@Brave words. Let's see you back them up with deeds, cur!"),
        (str_store_string_reg, s5, ":rand"),
      ], "{s5}", "close_window", []],
]
