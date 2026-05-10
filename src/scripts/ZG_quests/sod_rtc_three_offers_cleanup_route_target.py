SCRIPTS = [
("sod_rtc_three_offers_cleanup_route_target",
    [
      (quest_get_slot, ":target_party", "qst_rtc_companions_take_sides", slot_quest_target_party),
      (try_begin),
        (le, ":target_party", 0),
        (quest_get_slot, ":target_party", "qst_rtc_three_offers", slot_quest_target_party),
      (try_end),
      (try_begin),
        (gt, ":target_party", 0),
        (party_is_active, ":target_party"),
        (remove_party, ":target_party"),
      (try_end),
      (quest_set_slot, "qst_rtc_three_offers", slot_quest_target_party, -1),
      (quest_set_slot, "qst_rtc_three_offers", slot_quest_target_party_template, -1),
      (quest_set_slot, "qst_rtc_companions_take_sides", slot_quest_target_party, -1),
      (quest_set_slot, "qst_rtc_companions_take_sides", slot_quest_target_party_template, -1),
  ]),
]
