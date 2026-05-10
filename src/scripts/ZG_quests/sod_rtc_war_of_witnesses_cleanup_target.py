SCRIPTS = [
("sod_rtc_war_of_witnesses_cleanup_target",
    [
      (quest_get_slot, ":target_party", "qst_rtc_war_of_witnesses", slot_quest_target_party),
      (try_begin),
        (gt, ":target_party", 0),
        (party_is_active, ":target_party"),
        (remove_party, ":target_party"),
      (try_end),
      (quest_set_slot, "qst_rtc_war_of_witnesses", slot_quest_target_party, -1),
      (quest_set_slot, "qst_rtc_war_of_witnesses", slot_quest_target_party_template, -1),
  ]),
]
