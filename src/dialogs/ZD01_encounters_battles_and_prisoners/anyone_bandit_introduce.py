DIALOGS = [
[anyone, "bandit_introduce", [
      (store_random_in_range, ":rand", 11, 15),
        (str_store_string, s11, "@I can smell a fat purse a mile away. Methinks yours could do with some lightening, eh?"),
        (str_store_string, s12, "@Why, it be another traveller, chance met upon the road! I should warn you, country here's a mite dangerous for a good {fellow/woman} like you. But for a small donation my boys and I'll make sure you get rightways to your destination, eh?"),
        (str_store_string, s13, "@Well well, look at this! You'd best start coughing up some silver, friend, or me and my boys'll have to break you."),
    (str_store_string, s14, "@There's a toll for passin' through this land, payable to us, so if you don't mind we'll just be collectin' our due from your purse..."),
        (str_store_string_reg, s5, ":rand"),
    ], "{s5}", "bandit_talk", [(play_sound, "snd_encounter_bandits")]],
]
