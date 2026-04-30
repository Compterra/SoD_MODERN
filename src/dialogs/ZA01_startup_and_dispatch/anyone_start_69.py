DIALOGS = [
[anyone, "start",
   [
     (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_lady),
     (check_quest_active, "qst_duel_for_lady"),
     (check_quest_failed, "qst_duel_for_lady"),
     (quest_slot_eq, "qst_duel_for_lady", slot_quest_giver_troop, "$g_talk_troop"),
     (le, "$talk_context", tc_siege_commander),
     (quest_get_slot, ":quest_target_troop", "qst_duel_for_lady", slot_quest_target_troop),
     (call_script, "script_store_troop_name_link", s13, ":quest_target_troop"),
     ],
   "I was told that you sought satisfaction from {s13} to prove my innocence, {playername}.\
 It was a fine gesture, and I thank you for your efforts.", "lady_qst_duel_for_lady_failed", []],
]
