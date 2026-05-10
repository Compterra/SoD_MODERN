DIALOGS = [
[trp_rtc_imperial_courier, "start",
    [
      (check_quest_active, "qst_rtc_hound_sign"),
    ],
    "You should not have followed these tracks. The Hound does not bark before it bites, and couriers who lose seals lose more than pay.",
    "rtc_imperial_courier_talk",
    [
      (str_store_string, s49, "@An Imperial courier confirmed the Hound's secrecy: missing seals and route marks are enough to frighten even disciplined scouts."),

      (add_quest_note_from_sreg, "qst_rtc_hound_sign", 5, s49, 0),
    ]],
]
