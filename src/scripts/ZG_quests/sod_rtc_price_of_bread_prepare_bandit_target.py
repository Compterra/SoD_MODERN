SCRIPTS = [
("sod_rtc_price_of_bread_prepare_bandit_target",
    [
      (quest_get_slot, ":target_center", "qst_rtc_price_of_bread", slot_quest_target_center),
      (quest_get_slot, ":target_party", "qst_rtc_price_of_bread", slot_quest_target_party),
      (try_begin),
        (is_between, ":target_center", villages_begin, villages_end),
        (this_or_next|le, ":target_party", 0),
        (neg|party_is_active, ":target_party"),
        (set_spawn_radius, 4),
        (spawn_around_party, ":target_center", "pt_bandits"),
        (assign, ":target_party", reg0),
        (quest_set_slot, "qst_rtc_price_of_bread", slot_quest_target_party, ":target_party"),
        (quest_set_slot, "qst_rtc_price_of_bread", slot_quest_target_party_template, "pt_bandits"),
      (try_end),
  ]),
]
