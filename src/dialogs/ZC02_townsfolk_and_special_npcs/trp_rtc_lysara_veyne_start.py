DIALOGS = [
[trp_rtc_lysara_veyne, "start",
    [
      (check_quest_active, "qst_rtc_borrowed_names"),
    ],
    "Names are not truth. They are doors. Some open to pity, some to coin, some to command, and some to a knife in the dark. Which door should I write beside yours?",
    "rtc_lysara_veyne_talk",
    [
      (str_store_string, s49, "@Lysara Veyne warned that the player's public name would become the first door Calradia opens or closes."),

      (add_quest_note_from_sreg, "qst_rtc_borrowed_names", 4, s49, 0),
    ]],
]
