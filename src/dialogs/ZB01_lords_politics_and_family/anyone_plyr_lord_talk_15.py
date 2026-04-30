DIALOGS = [
[anyone|plyr, "lord_talk",
    [
      (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
      (lt, "$g_talk_troop_faction_relation", 0),
      (this_or_next|eq, "$players_kingdom", 0),
      (eq, "$players_kingdom", "fac_player_supporters_faction"),
      #MORDACHAI - allow one to burry the hatchet with their former king
      #(neq, "$players_oath_renounced_against_kingdom", "$g_talk_troop_faction"),
      (assign, ":continue", 1),
      (try_begin),
        (gt, "$supported_pretender", 0),
        (eq, "$supported_pretender_old_faction", "$g_talk_troop_faction"),
        (assign, ":continue", 0),
      (try_end),
      (eq, ":continue", 1),
      (str_store_faction_name, s4, "$g_talk_troop_faction"),

      #MORDACHAI - generate a wider range of responses to the player, with his persuasion skill, charisma, et. al. factors involved
      (store_attribute_level, ":charisma", "trp_player", ca_charisma),
      (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
      (store_mul, ":upper_bound", ":persuasion", 10),
      (val_add, ":upper_bound", ":charisma"),
      (val_add, ":upper_bound", 1), #compensate for the range stupidity of the random function
      (assign, ":lower_bound", "$g_talk_troop_relation"),
      (store_random_in_range, reg10, ":lower_bound", ":upper_bound"),
   ],
   "I wish to make peace with {s4}.", "lord_ask_pardon", []],
]
