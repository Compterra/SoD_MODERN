DIALOGS = [
[anyone, "gm_tell_mission", [(eq, "$random_quest_no", "qst_slavers_bring_back_runaway_slaves"),
  (quest_set_slot, "$random_quest_no", slot_quest_target_center, "$g_encountered_party"),
  (str_store_party_name_link, s4, "$g_encountered_party"),
  ],
 "Three groups of my slaves have broken free due to the stupidity of some incompetent slave drivers. We don't want them to run around and spread rumors of business, now do we? They are confused by their new situation and they should still be close to {s4}. Round them up and whip them back to their cages. We won't be ungrateful... so?", "gm_bring_back_runaway_slaves",
   [
    ]],
]
