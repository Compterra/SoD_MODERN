DIALOGS = [
[trp_rtc_celeste_di_marina, "start",
    [
      (check_quest_active, "qst_rtc_price_of_bread"),
    ],
    "Grain is not mercy in a sack. It is carts, guards, weights, spoilage, debt, and someone blamed when the last loaf is gone. If you want supply, do not insult the people who can move it.",
    "rtc_celeste_di_marina_talk",
    [
      (str_store_string, s49, "@Celeste di Marina argued the merchant side: grain needs contracts, transport, and trust, not only pity."),

      (add_quest_note_from_sreg, "qst_rtc_price_of_bread", 5, s49, 0),
    ]],
]
