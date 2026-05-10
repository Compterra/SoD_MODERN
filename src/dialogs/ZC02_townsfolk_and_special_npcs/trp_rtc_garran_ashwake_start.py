DIALOGS = [
[trp_rtc_garran_ashwake, "start",
    [
      (this_or_next|check_quest_active, "qst_rtc_last_smoke"),
      (check_quest_active, "qst_rtc_hound_sign"),
    ],
    "Stand where I can see you. If the road is burning behind us, then every breath we waste has a body tied to it. Tell me what survived, and I will tell you what can still be defended.",
    "rtc_garran_ashwake_talk",
    [
      (str_store_string, s49, "@Sir Garran Ashwake took command of the survivors' defense and demanded a clear accounting of what survived the burned road."),

      (add_quest_note_from_sreg, "qst_rtc_last_smoke", 4, s49, 0),
    ]],
]
