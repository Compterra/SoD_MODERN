SCRIPTS = [
("sod_rtc_hounds_terms_cleanup_envoy",
    [
      (quest_get_slot, ":envoy_party", "qst_rtc_hounds_terms", slot_quest_target_party),
      (try_begin),
        (gt, ":envoy_party", 0),
        (party_is_active, ":envoy_party"),
        (remove_party, ":envoy_party"),
      (try_end),
      (quest_set_slot, "qst_rtc_hounds_terms", slot_quest_target_party, -1),
      (quest_set_slot, "qst_rtc_hounds_terms", slot_quest_target_party_template, -1),
  ]),
]
