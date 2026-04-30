DIALOGS = [
[anyone, "lost_kidnapped_girl_3", [],
   "You let me down {playername}. I had trusted you.\
 I will let people know of your incompetence at this task.\
 Also, I want back that {reg8} denars I gave you as the ransom fee.", "lost_kidnapped_girl_4",
   [(quest_get_slot, reg8, "qst_kidnapped_girl", slot_quest_target_amount),
    (try_for_parties, ":cur_party"),
      (party_count_members_of_type, ":num_members", ":cur_party", "trp_kidnapped_girl"),
      (gt, ":num_members", 0),
      (party_remove_members, ":cur_party", "trp_kidnapped_girl", 1),
      (party_remove_prisoners, ":cur_party", "trp_kidnapped_girl", 1),
    (try_end),
    (call_script, "script_end_quest", "qst_kidnapped_girl"),
    (call_script, "script_change_troop_renown", "trp_player", -5),
    ]],
]
