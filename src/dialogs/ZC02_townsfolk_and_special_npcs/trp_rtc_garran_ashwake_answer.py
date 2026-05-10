DIALOGS = [
[trp_rtc_garran_ashwake, "rtc_garran_ashwake_answer", [],
    "Look for what soldiers cannot help but leave behind: ration marks, route ash, courier seals, hoof discipline. Panic lies. Logistics tells the truth.",
    "close_window",
    [
      (try_begin),
        (check_quest_active, "qst_rtc_hound_sign"),
        (str_store_string, s49, "@Garran advised reading the Imperial advance through logistics: ration marks, route ash, courier seals, and disciplined hoof tracks."),

        (add_quest_note_from_sreg, "qst_rtc_hound_sign", 4, s49, 0),
      (try_end),
    ]],
]
