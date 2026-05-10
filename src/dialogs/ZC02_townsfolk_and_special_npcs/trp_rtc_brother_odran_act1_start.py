DIALOGS = [
[trp_rtc_brother_odran, "start",
    [
      (this_or_next|check_quest_active, "qst_rtc_last_smoke"),
      (check_quest_active, "qst_rtc_borrowed_names"),
    ],
    "Smoke makes all faces equal at first. Then choices return their names. Save who you can, and do not let hurry teach you to stop seeing people.",
    "rtc_brother_odran_act1_talk",
    [
      (str_store_string, s49, "@Brother Odran urged mercy on the burned road: speed matters, but survivors must not become cargo in the player's mind."),

      (add_quest_note_from_sreg, "qst_rtc_last_smoke", 5, s49, 0),
    ]],
]
