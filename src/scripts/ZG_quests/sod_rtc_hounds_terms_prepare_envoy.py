SCRIPTS = [
("sod_rtc_hounds_terms_prepare_envoy",
    [
      (quest_get_slot, ":envoy_party", "qst_rtc_hounds_terms", slot_quest_target_party),
      (try_begin),
        (this_or_next|le, ":envoy_party", 0),
        (neg|party_is_active, ":envoy_party"),
        (call_script, "script_sod_rtc_prepare_temporary_target", "qst_rtc_hounds_terms", "pt_sod_diplomatic_envoy", "p_main_party", 2, 0),
      (try_end),
  ]),
]
