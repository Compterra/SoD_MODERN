DIALOGS = [
[trp_sod_marshal, "marshal_upgrade_garrison_check",
    [
      # only present this if there are NO troops to upgrade at all...
      (assign, ":total", 0),
      (try_for_range, ":troop_no", "trp_experience_troop", "trp_last_troop"),
        (party_count_companions_of_type, ":troop_count", "$g_encountered_party", ":troop_no"),
        (val_add, ":total", ":troop_count"),
      (try_end),
      (eq, ":total", 0),
    ], "None of your troops are ready to upgrade, my liege.  Please return to me when your troops have become more experienced.", "marshal_talk_again", []],
]
