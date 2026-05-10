DIALOGS = [
[trp_rtc_tamsin_reedhand, "start",
    [
      (check_quest_active, "qst_rtc_price_of_bread"),
    ],
    "You bring hungry people to my door and call it need. I have buried hungry people here before, {sir/madam}. Tell me why your road should eat before my village.",
    "rtc_tamsin_reedhand_talk",
    [
      (str_store_string, s49, "@Tamsin Reedhand spoke for the village: grain given to refugees may become graves among her own people if the price is wrong."),

      (add_quest_note_from_sreg, "qst_rtc_price_of_bread", 4, s49, 0),
    ]],
]
