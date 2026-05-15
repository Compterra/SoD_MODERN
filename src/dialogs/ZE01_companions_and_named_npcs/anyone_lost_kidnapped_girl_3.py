DIALOGS = [
[anyone, "lost_kidnapped_girl_3", [
   (check_quest_active, "qst_kidnapped_girl"),
   (neg|check_quest_concluded, "qst_kidnapped_girl"),
   (quest_get_slot, reg8, "qst_kidnapped_girl", slot_quest_target_amount),
],
   "You let me down {playername}. I had trusted you.\
 I will let people know of your incompetence at this task.\
 Also, I want back that {reg8} denars I gave you as the ransom fee.", "lost_kidnapped_girl_4",
   [(quest_get_slot, "$g_sod_lost_rescue_repayment_amount", "qst_kidnapped_girl", slot_quest_target_amount),
    (try_begin),
      (check_quest_active, "qst_kidnapped_girl"),
      (neg|check_quest_concluded, "qst_kidnapped_girl"),
      (try_for_parties, ":cur_party"),
        (party_count_members_of_type, ":num_members", ":cur_party", "trp_kidnapped_girl"),
        (party_count_prisoners_of_type, ":num_prisoners", ":cur_party", "trp_kidnapped_girl"),
        (val_add, ":num_members", ":num_prisoners"),
        (gt, ":num_members", 0),
        (party_remove_members, ":cur_party", "trp_kidnapped_girl", 1),
        (party_remove_prisoners, ":cur_party", "trp_kidnapped_girl", 1),
      (try_end),
      (call_script, "script_end_quest", "qst_kidnapped_girl"),
      (call_script, "script_change_troop_renown", "trp_player", -5),
    (else_try),
      (display_message, "@The lost kidnapped-girl report could not be completed because the quest is no longer active.", 0xFF6666),
    (try_end),
    ]],
]
