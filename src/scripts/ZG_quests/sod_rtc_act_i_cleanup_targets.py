SCRIPTS = [
("sod_rtc_act_i_cleanup_targets",
    [
      (try_for_range, ":quest_no", "qst_rtc_last_smoke", "qst_rtc_price_of_bread"),
        (quest_get_slot, ":target_party", ":quest_no", slot_quest_target_party),
        (try_begin),
          (gt, ":target_party", 0),
          (neq, ":target_party", "p_main_party"),
          (party_is_active, ":target_party"),
          (remove_party, ":target_party"),
        (try_end),
        (quest_set_slot, ":quest_no", slot_quest_target_party, -1),
        (quest_set_slot, ":quest_no", slot_quest_target_party_template, -1),
      (try_end),
  ]),
]
