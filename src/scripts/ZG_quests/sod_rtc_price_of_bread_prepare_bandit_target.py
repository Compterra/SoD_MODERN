SCRIPTS = [
("sod_rtc_price_of_bread_prepare_bandit_target",
    [
      (quest_get_slot, ":target_center", "qst_rtc_price_of_bread", slot_quest_target_center),
      (quest_get_slot, ":target_party", "qst_rtc_price_of_bread", slot_quest_target_party),
      (try_begin),
        (is_between, ":target_center", villages_begin, villages_end),
        (this_or_next|le, ":target_party", 0),
        (neg|party_is_active, ":target_party"),
        (call_script, "script_sod_rtc_prepare_temporary_target", "qst_rtc_price_of_bread", "pt_bandits", ":target_center", 4, 0),
      (try_end),
  ]),
]
