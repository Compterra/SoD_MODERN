DIALOGS = [
[trp_rtc_brother_odran, "start",
    [
      (check_quest_active, "qst_rtc_price_of_bread"),
    ],
    "I have seen men die after victory because nobody counted the mouths victory brought home. Bread is not a small matter. It is the first law people believe.",
    "rtc_brother_odran_talk",
    [
      (str_store_string, s49, "@Brother Odran warned that mercy must become a working law quickly, or the refugees will learn that survival has no shepherd."),

      (add_quest_note_from_sreg, "qst_rtc_price_of_bread", 6, s49, 0),
    ]],
]
