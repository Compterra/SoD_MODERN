SCRIPTS = [
("sod_quest_journal_mark_pinned",
    [
      (store_script_param, ":quest_no", 1),
      (store_script_param, ":pinned", 2),
      (quest_get_slot, ":flags", ":quest_no", slot_quest_sod_journal_flags),
      (try_begin),
        (gt, ":pinned", 0),
        (val_or, ":flags", sod_quest_journal_flag_pinned),
      (else_try),
        (store_sub, ":not_pin_mask", 255, sod_quest_journal_flag_pinned),
        (store_and, ":flags", ":flags", ":not_pin_mask"),
      (try_end),
      (quest_set_slot, ":quest_no", slot_quest_sod_journal_flags, ":flags"),
  ]),
]
