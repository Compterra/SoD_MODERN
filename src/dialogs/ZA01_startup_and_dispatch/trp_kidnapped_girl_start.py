DIALOGS = [
[trp_kidnapped_girl, "start",
   [
     (eq, "$talk_context", tc_entering_center_quest_talk),
     ],
   "Thank you so much for bringing me back!\
  I can't wait to see my family. Good-bye.",
   "close_window",
   [(remove_member_from_party, "trp_kidnapped_girl"),
    (quest_set_slot, "qst_kidnapped_girl", slot_quest_current_state, 4),
    ]],
]
