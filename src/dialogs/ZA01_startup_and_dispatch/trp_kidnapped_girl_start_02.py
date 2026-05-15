DIALOGS = [
[trp_kidnapped_girl, "start", [
   (check_quest_active, "qst_kidnapped_girl"),
   (neg|check_quest_concluded, "qst_kidnapped_girl"),
   (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 3),
],
   "Oh {sir/madam}. Thank you so much for rescuing me. Will you take me to my family now?", "kidnapped_girl_liberated_map", []],
]
