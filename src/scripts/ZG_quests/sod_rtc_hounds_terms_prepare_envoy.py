SCRIPTS = [
("sod_rtc_hounds_terms_prepare_envoy",
    [
      (quest_get_slot, ":envoy_party", "qst_rtc_hounds_terms", slot_quest_target_party),
      (try_begin),
        (this_or_next|le, ":envoy_party", 0),
        (neg|party_is_active, ":envoy_party"),
        (set_spawn_radius, 2),
        (spawn_around_party, "p_main_party", "pt_sod_diplomatic_envoy"),
        (assign, ":envoy_party", reg0),
        (quest_set_slot, "qst_rtc_hounds_terms", slot_quest_target_party, ":envoy_party"),
        (quest_set_slot, "qst_rtc_hounds_terms", slot_quest_target_party_template, "pt_sod_diplomatic_envoy"),
      (try_end),
  ]),
]
